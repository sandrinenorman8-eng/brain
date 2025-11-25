from flask import Blueprint, request
from utils.response_utils import success_response, error_response
from services.search_service import search_content

search_bp = Blueprint('search', __name__, url_prefix='/api')

@search_bp.route('/search_content', methods=['POST'])
def search_route():
    try:
        data = request.get_json()
        search_term = data.get('term', '')
        
        if not search_term:
            return error_response("Search term is required", 400)
        
        results = search_content(search_term)
        return success_response(results)
    
    except ConnectionError as e:
        return error_response(str(e), 503, "ServiceUnavailable")
    except TimeoutError as e:
        return error_response(str(e), 504, "GatewayTimeout")
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500, "InternalServerError")

# Route sans préfixe pour compatibilité
@search_bp.route('/search_content', methods=['POST'])
def search_route_compat():
    return search_route()
