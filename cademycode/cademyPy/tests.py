import pytest

from cleaner import Clean


@pytest.fixture
def raw_load():
    clean= Clean("./cademycode/cademyPy/setting.json")
    clean.load_data()
    return clean

@pytest.fixture
def student_clean():
    clean= Clean("./cademycode/cademyPy/setting.json")
    clean.load_data()
    clean.clean_student_table()
    return clean

@pytest.fixture
def merged_clean():
    clean= Clean("./cademycode/cademyPy/setting.json")
    clean.load_data()
    clean.clean_student_table()
    clean.merge_tables()
    return clean

def test_tables(raw_load):
    clean=raw_load
    assert "cademycode_courses" in clean.table_lst
    assert "cademycode_student_jobs" in clean.table_lst
    assert "cademycode_students" in clean.table_lst

def test_merge_columns(raw_load):
    clean=raw_load
    assert "job_id" in clean.get_colums("cademycode_students")
    assert "current_career_path_id" in clean.get_colums("cademycode_students")
    assert "job_id" in clean.get_colums("cademycode_student_jobs")
    assert "career_path_id" in clean.get_colums("cademycode_courses")

def test_data_conversion(student_clean):
    clean=student_clean
    for col in clean.get_colums("cademycode_students"):
        assert col in ['uuid', 'dob', 'sex', 'job_id', 'num_course_taken',
        'current_career_path_id', 'time_spent_hrs', 'first_name', 'last_name',
        'street', 'city', 'state', 'zip', 'email']

def test_merge_cols(merged_clean):
    clean=merged_clean
    for col in clean.big_df.columns:
        assert col in ['uuid', 'dob', 'sex', 'num_course_taken', 'current_career_path_id',
            'time_spent_hrs', 'first_name', 'last_name', 'street', 'city', 'state',
            'zip', 'email', 'career_path_name', 'hours_to_complete', 'job_category',
            'avg_salary']