import os
import pytest

import calculation

is_release = False

class TestCal(object):

    @classmethod
    def setup_class(cls):
        print('start')
        cls.cal = calculation.Cal()
        cls.test_dir = '/tmp/test_dir'
        cls.test_file_name = 'test.txt'

    @classmethod
    def teardown_class(cls):
        import shutil
        if os.path.exists(cls.test_dir):
            shutil.rmtree(cls.test_dir)
        print('end')
        del cls.cal

    def setup_method(self, method):
        print('method={}'.format(method.__name__))
        # self.cal = calculation.Cal()

    def teardown_method(self, method):
        print('method={}'.format(method.__name__))
        # del self.cal

    def test_save_no_dir(self):
        self.cal.save(self.test_dir, self.test_file_name)
        test_file_path = os.path.join(self.test_dir, self.test_file_name)
        assert os.path.exists(test_file_path) is True

    # @pytest.mark.skip(is_release==True, reason='because I want to skip this time')
    def test_add_num_and_double(self, tmpdir, csv_file):
        print('tmpdir: <', tmpdir, '>')
        print(csv_file)
        assert self.cal.add_num_and_double(1, 1) == 4

    def test_add_num_and_double_raise(self):
        with pytest.raises(ValueError):
            self.cal.add_num_and_double('1', '1')

    def test_save(self, tmpdir):
        self.cal.save(tmpdir, self.test_file_name)
        test_file_path = os.path.join(tmpdir, self.test_file_name)
        assert os.path.exists(test_file_path) is True
