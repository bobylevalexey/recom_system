import os

FOOD_CATEGORIES = [
    'dosug_razvlecheniya_obshhestvennoe_pitanie/kombinaty_pitaniya',
    'dosug_razvlecheniya_obshhestvennoe_pitanie/piccerii',
    'dosug_razvlecheniya_obshhestvennoe_pitanie/stolovye',
    'dosug_razvlecheniya_obshhestvennoe_pitanie/bary',
    'dosug_razvlecheniya_obshhestvennoe_pitanie/kafe',
    'dosug_razvlecheniya_obshhestvennoe_pitanie/kafe_konditerskie_kofejjni',
    ('dosug_razvlecheniya_obshhestvennoe_pitanie/'
     'kafe_restorany_bystrogo_pitaniya'),
    'dosug_razvlecheniya_obshhestvennoe_pitanie/kulinariya',
    'dosug_razvlecheniya_obshhestvennoe_pitanie/restorany',
    'dosug_razvlecheniya_obshhestvennoe_pitanie/sushi_bary_restorany',
    ('dosug_razvlecheniya_obshhestvennoe_pitanie/'
     'fresh_bary_tochki_bezalkogolnykh_koktejjlejj_goryachikh_napitkov'),
    'dosug_razvlecheniya_obshhestvennoe_pitanie/chajjnye_kluby',
    'dosug_razvlecheniya_obshhestvennoe_pitanie/centry_parovykh_koktejjlejj'
]

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
ML_DATA_DIR = os.path.join(DATA_DIR, 'movielens_data')

SVD_TRAIN_SET_FILE = os.path.join(DATA_DIR, 'svd_train.arr')
SVD_TEST_SET_FILE = os.path.join(DATA_DIR, 'svd_test.arr')

SVD_TRAIN_SET_CSV_FILE = os.path.join(DATA_DIR, 'svd_train.csv')
SVD_TEST_SET_CSV_FILE = os.path.join(DATA_DIR, 'svd_test.csv')
