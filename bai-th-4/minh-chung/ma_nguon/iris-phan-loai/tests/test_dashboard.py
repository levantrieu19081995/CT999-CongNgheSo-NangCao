from pathlib import Path
from io import BytesIO
import sys
import pytest
from pypdf import PdfReader
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from dashboard_data import load_snapshot, filter_species, filtered_pdf


def test_filters_and_export_keep_selected_rows():
    raw, clean, metrics, summary = load_snapshot(ROOT)
    assert len(raw) == 150 and len(clean) == 147
    selected = filter_species(clean, ['Iris-setosa'])
    assert len(selected) == 48
    assert set(selected.species) == {'Iris-setosa'}
    pdf = filtered_pdf(selected, 'petal_length', 'petal_width', metrics, summary)
    document = PdfReader(BytesIO(pdf))
    assert len(document.pages) == 2
    text = '\n'.join(p.extract_text() for p in document.pages)
    assert 'Số mẫu theo bộ lọc: 48' in text
    assert 'Kết quả mô hình trên toàn bộ dữ liệu' in text
    assert '102' in text and '45' in text


def test_export_rejects_empty_filter_and_invalid_axis():
    _, clean, metrics, summary = load_snapshot(ROOT)
    with pytest.raises(ValueError, match='ít nhất một loài'):
        filtered_pdf(filter_species(clean, []), 'petal_length', 'petal_width', metrics, summary)
    with pytest.raises(ValueError, match='thuộc tính'):
        filtered_pdf(clean, 'source_id', 'species', metrics, summary)


def test_app_updates_counts_and_axes():
    app = AppTest.from_file(str(ROOT/'src/dashboard.py'), default_timeout=30).run()
    assert not app.exception
    assert app.metric[0].value == '147'
    app.multiselect(key='species').set_value(['Iris-setosa']).run()
    assert not app.exception
    assert app.metric[0].value == '48'
    assert app.metric[1].value == '1'
    app.selectbox(key='x_feature').set_value('sepal_length').run()
    assert not app.exception
    assert app.selectbox(key='x_feature').value == 'sepal_length'
    assert any('48' in p.value for p in app.caption)


def test_app_handles_no_species_without_stale_data():
    app = AppTest.from_file(str(ROOT/'src/dashboard.py'), default_timeout=30).run()
    app.multiselect(key='species').set_value([]).run()
    assert not app.exception
    assert app.metric[0].value == '0'
    assert app.warning and 'Chọn ít nhất một loài' in app.warning[0].value


def test_all_chart_types_render_for_a_subset():
    app = AppTest.from_file(str(ROOT/'src/dashboard.py'), default_timeout=30).run()
    app.multiselect(key='species').set_value(['Iris-versicolor', 'Iris-virginica']).run()
    assert app.metric[0].value == '99'
    for chart in ['Phân bố', 'Tương quan', 'Phân tán']:
        app.radio(key='chart_type').set_value(chart).run()
        assert not app.exception
        assert app.metric[0].value == '99'
