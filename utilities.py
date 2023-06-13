def validate_required_fields(fields: dict) -> dict:
    return {
        'detail': f'Field {field} is required'
        for field in fields
        if fields.get(field) is None or fields.get(field) == '' or fields.get(field) == []
    }


def get_authenticated_email(request):
    try:
        if request.auth.get('email') is not None:  # Token User
            return request.auth.get('email')
    except Exception as e:
        return str(e)
