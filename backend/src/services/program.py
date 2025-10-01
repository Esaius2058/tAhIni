import logging
from sqlalchemy.orm import Session
from backend.src.db.models import Program
from backend.src.services.questions import ServiceError, NotFoundError

class ProgramService:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.logger = logging.getLogger("Program Service")

    def create_program(self, name: str, description: str, duration_years: int = 4):
        try:
            program = Program(name=name, description=description, duration_years=duration_years)
            self.db.add(program)
            self.db.commit()
            self.db.refresh(program)
            return program
        except Exception as e:
            self.logger.error(f"Create program failed: {e}")
            raise ServiceError("Could not create program") from e

    def get_program(self, program_id: str):
        try:
            program = self.db.query(Program).filter(Program.id == program_id).first()
            if not program:
                raise NotFoundError("Program not found")
            return program
        except NotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"Get program failed: {e}")
            raise ServiceError("Could not fetch program") from e

    def update_program(self, program_id: str, **kwargs):
        try:
            program = self.get_program(program_id)
            for key, value in kwargs.items():
                setattr(program, key, value)
            self.db.commit()
            self.db.refresh(program)
            return program
        except NotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"Update program failed: {e}")
            raise ServiceError("Could not update program") from e

    def list_programs(self, limit: int = 25, offset: int = 0):
        try:
            programs = self.db.query(Program).limit(limit).offset(offset)

            return [{
                "program_id": program.id,
                "program_name": program.name,
                "program_description": program.description,
                "program_duration": program.duration_years
            } for program in programs
            ]
        except Exception as e:
            self.logger.error(f"List programs failed: {e}")
            raise ServiceError("Could not list programs") from e

    def delete_program(self, program_id: str):
        try:
            program = self.get_program(program_id)
            self.db.delete(program)
            self.db.commit()
            return True
        except NotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"Delete program failed: {e}")
            raise ServiceError("Could not delete program") from e
