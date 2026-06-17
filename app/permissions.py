from fastapi import HTTPException


def is_admin(current_user):

    return current_user["role"] == "admin"


def verify_patient_access(
    current_user,
    patient_id
):

    if is_admin(current_user):
        return True

    if current_user["role"] == "patient":

        if current_user["id"] != patient_id:

            raise HTTPException(
                status_code=403,
                detail="Access Denied"
            )

    return True