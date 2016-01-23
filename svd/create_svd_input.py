from model import session_scope
from tables import FlampMarksTable, FoodEkbFirms


def get_marks_list_from_db():
    with session_scope() as sess:
        return sess.query(
                FlampMarksTable.firm_id, FlampMarksTable.expert_id,
                FlampMarksTable.mark
        ).join(
                FoodEkbFirms, FoodEkbFirms.food_pk == FlampMarksTable.firm_id
        ).all()
