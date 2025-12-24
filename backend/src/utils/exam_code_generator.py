import secrets
import string

def generate_exam_code(exam_type: str, course_code: str) -> str:
    rand = ''.join(
        secrets.choice(string.ascii_letters + string.digits)
        for _ in range(5)
    )
    return f"{exam_type.upper()}-{course_code.upper()}-{rand}"
