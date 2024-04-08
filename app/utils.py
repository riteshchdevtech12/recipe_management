
class FieldValidator:
    @staticmethod
    def check_required_fields(data, required_fields):
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            response = {
                'status': 'error',
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }
            return response, 400
        return None, None
