/** Đọc Markdown, tạo slide theo từng tiêu đề ## và xuất PowerPoint. */
import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';

const require = createRequire(import.meta.url);
const { Presentation, PresentationFile } = await import(pathToFileURL(require.resolve('@oai/artifact-tool')).href);

function readCsv(text) {
  const rows=[]; let row=[],field='',quoted=false;
  for(let i=0;i<text.length;i++) {
    const c=text[i];
    if(c==='"' && text[i+1]==='"' && quoted) {field+='"';i++;}
    else if(c==='"') quoted=!quoted;
    else if(c===',' && !quoted) {row.push(field);field='';}
    else if(c==='\n' && !quoted) {row.push(field.replace(/\r$/,''));if(row.some(Boolean)) rows.push(row);row=[];field='';}
    else field+=c;
  }
  if(field || row.length) {row.push(field);rows.push(row);}
  const header=rows.shift().map(s=>s.replace(/^\uFEFF/,''));
  return rows.map(r=>Object.fromEntries(header.map((h,i)=>[h,r[i]])));
}

function parseMarkdown(text) {
  const sections=[]; let current=null;
  for(const raw of text.split(/\r?\n/)) {
    const heading=raw.match(/^(#{1,2})\s+(.+)$/);
    if(heading) {current={title:heading[2],cover:heading[1]==='#',lines:[],notes:[],assets:[]};sections.push(current);continue;}
    if(!current || !raw.trim())continue;
    const command=raw.match(/^<!--\s*(source|chart-csv|table-csv):\s*(.*?)\s*-->$/);
    if(command) {if(command[1]==='source')current.notes.push(command[2]);else current.assets.push({kind:command[1],file:command[2]});continue;}
    const image=raw.match(/^!\[([^\]]*)\]\(([^)]+)\)$/);
    if(image) {current.assets.push({kind:'image',file:image[2],alt:image[1]});continue;}
    current.lines.push(raw.replace(/^[-*]\s+/,''));
  }
  if(!sections.length)throw new Error('Tệp Markdown cần ít nhất một tiêu đề # hoặc ##.');
  for(const s of sections) {
    if(s.title.length>85)throw new Error('Tiêu đề quá dài: '+s.title);
    if(s.lines.join('').length>800)throw new Error('Nội dung quá dài cho một slide: '+s.title);
    if(s.assets.length>1)throw new Error('Mỗi mục hiện hỗ trợ một hình, bảng hoặc biểu đồ.');
  }
  return sections;
}

function textbox(slide,text,x,y,w,h,size=30,bold=false,color='#182d3b') {
  const box=slide.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
  box.text=text;
  box.text.style={typeface:'Arial',fontSize:size,bold,color};
  return box;
}

async function makeDeck(input,output,previewDir) {
  const sections=parseMarkdown(await fs.readFile(input,'utf8'));
  const p=Presentation.create({slideSize:{width:1280,height:720}});
  for(let i=0;i<sections.length;i++) {
    const s=sections[i],slide=p.slides.add();slide.background.fill='#ffffff';
    textbox(slide,s.title,72,s.cover?140:52,1136,s.cover?190:102,s.cover?58:44,true,'#173e53');
    if(s.cover) textbox(slide,s.lines.join('\n\n'),76,365,1090,230,30);
    else if(!s.assets.length) textbox(slide,s.lines.join('\n\n'),76,190,1110,430,30);
    else {
      const asset=s.assets[0];const file=path.resolve(path.dirname(input),asset.file);
      if(asset.kind==='image') {
        slide.images.add({blob:new Uint8Array(await fs.readFile(file)),contentType:'image/png',alt:asset.alt,fit:'contain',position:{left:72,top:170,width:690,height:470}});
        textbox(slide,s.lines.join('\n\n'),805,200,385,380,28);
      } else {
        const rows=readCsv(await fs.readFile(file,'utf8'));
        if(!rows.length)throw new Error('CSV rỗng: '+file);
        if(asset.kind==='chart-csv') {
          slide.charts.add('bar',{
            position:{left:95,top:180,width:1040,height:385},
            categories:rows.map(r=>r.model),series:[{name:'F1 macro CV',values:rows.map(r=>Number(r.cv_f1_mean)),fill:'#286b9a'}],
            hasLegend:false,barOptions:{direction:'column',grouping:'clustered',gapWidth:100},
            xAxis:{textStyle:{typeface:'Arial',fontSize:22}},
            yAxis:{min:0,max:1.05,numberFormatCode:'0.0',textStyle:{typeface:'Arial',fontSize:22},majorGridlines:{fill:'#d9e0e6',width:1}},
            dataLabels:{showValue:true,position:'outEnd',numberFormatCode:'0.0000',textStyle:{typeface:'Arial',fontSize:23}},
          });
          textbox(slide,s.lines.join('\n'),90,595,1100,70,24);
        } else {
          const values=[['Mô hình','F1 CV','Accuracy test','F1 macro test','Đúng/tổng'],...rows.map(r=>[r.model,Number(r.cv_f1_mean).toFixed(4),Number(r.test_accuracy).toFixed(4),Number(r.test_f1_macro).toFixed(4),r.correct+'/'+r.test_n])];
          const t=slide.tables.add({rows:values.length,columns:5,left:72,top:200,width:1136,height:300,columnWidths:[280,180,230,250,196],values});
          t.borders.assign({fill:'#c6cfd5',width:1});
          for(let r=0;r<values.length;r++)for(let c=0;c<5;c++) {
            const cell=t.getCell(r,c);cell.fill=r===0?'#e7eef3':'#ffffff';
            cell.text.style={typeface:'Arial',fontSize:24,bold:r===0,color:'#182d3b'};
          }
          textbox(slide,s.lines.join('\n\n'),80,550,1120,100,26);
        }
      }
    }
    slide.speakerNotes.text=[...s.notes,'Nội dung đầu vào: '+path.basename(input),...s.lines].join('\n');
    textbox(slide,String(i+1),1180,666,35,25,18,false,'#6b747c');
  }
  await fs.mkdir(path.dirname(output),{recursive:true});
  await (await PresentationFile.exportPptx(p)).save(output);
  if(previewDir) {
    await fs.mkdir(previewDir,{recursive:true});
    for(const [i,slide] of p.slides.items.entries()) {
      const png=await p.export({slide,format:'png',scale:1});
      await fs.writeFile(path.join(previewDir,`slide-${i+1}.png`),new Uint8Array(await png.arrayBuffer()));
    }
  }
  console.log('Đầu vào:',input);
  console.log('Số mục Markdown / số slide:',sections.length,'/',p.slides.items.length);
  console.log('Đã tạo PowerPoint:',output);
}

const args=process.argv.slice(2);
const input=path.resolve(args[0]||'docs/noi_dung_slide.md');
const output=path.resolve(args[1]||'results/Thuyet_trinh_Iris.pptx');
await makeDeck(input,output,args[2]?path.resolve(args[2]):null);
