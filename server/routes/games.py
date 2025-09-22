from flask import jsonify, Response, Blueprint, request
from models import db, Game, Publisher, Category
from sqlalchemy.orm import Query
from sqlalchemy.exc import IntegrityError

# Create a Blueprint for games routes
games_bp = Blueprint('games', __name__)

def get_games_base_query() -> Query:
    return db.session.query(Game).join(
        Publisher, 
        Game.publisher_id == Publisher.id, 
        isouter=True
    ).join(
        Category, 
        Game.category_id == Category.id, 
        isouter=True
    )

@games_bp.route('/api/games', methods=['GET'])
def get_games() -> Response:
    # Use the base query for all games
    games_query = get_games_base_query().all()
    
    # Convert the results using the model's to_dict method
    games_list = [game.to_dict() for game in games_query]
    
    return jsonify(games_list)

@games_bp.route('/api/games/<int:id>', methods=['GET'])
def get_game(id: int) -> tuple[Response, int] | Response:
    # Use the base query and add filter for specific game
    game_query = get_games_base_query().filter(Game.id == id).first()
    
    # Return 404 if game not found
    if not game_query: 
        return jsonify({"error": "Game not found"}), 404
    
    # Convert the result using the model's to_dict method
    game = game_query.to_dict()
    
    return jsonify(game)

@games_bp.route('/api/games', methods=['POST'])
def create_game() -> tuple[Response, int]:
    """Create a new game"""
    try:
        # Get JSON data from request - handle potential JSON errors
        try:
            data = request.get_json(force=True)
        except Exception:
            return jsonify({"error": "Request body must be valid JSON"}), 400
        
        # Validate required fields
        if not data:
            return jsonify({"error": "Request body must be valid JSON"}), 400
            
        required_fields = ['title', 'description', 'category_id', 'publisher_id']
        missing_fields = [field for field in required_fields if field not in data or data[field] is None]
        
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
        
        # Validate that publisher and category exist
        publisher = Publisher.query.get(data['publisher_id'])
        if not publisher:
            return jsonify({"error": "Publisher not found"}), 404
            
        category = Category.query.get(data['category_id'])
        if not category:
            return jsonify({"error": "Category not found"}), 404
        
        # Create new game instance
        game = Game(
            title=data['title'],
            description=data['description'],
            category_id=data['category_id'],
            publisher_id=data['publisher_id'],
            star_rating=data.get('star_rating')  # Optional field
        )
        
        # Add to database
        db.session.add(game)
        db.session.commit()
        
        # Return the created game with full details
        created_game = get_games_base_query().filter(Game.id == game.id).first()
        return jsonify(created_game.to_dict()), 201
        
    except ValueError as e:
        # Handle validation errors from model validators
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except IntegrityError as e:
        # Handle database integrity errors
        db.session.rollback()
        return jsonify({"error": "Database integrity error"}), 400
    except Exception as e:
        # Handle unexpected errors
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500

@games_bp.route('/api/games/<int:id>', methods=['PUT'])
def update_game(id: int) -> tuple[Response, int]:
    """Update an existing game"""
    try:
        # Find the game to update
        game = Game.query.get(id)
        if not game:
            return jsonify({"error": "Game not found"}), 404
        
        # Get JSON data from request - handle potential JSON errors
        try:
            data = request.get_json(force=True)
        except Exception:
            return jsonify({"error": "Request body must be valid JSON"}), 400
        
        if not data:
            return jsonify({"error": "Request body must be valid JSON"}), 400
        
        # Validate publisher and category if provided
        if 'publisher_id' in data and data['publisher_id'] is not None:
            publisher = Publisher.query.get(data['publisher_id'])
            if not publisher:
                return jsonify({"error": "Publisher not found"}), 404
                
        if 'category_id' in data and data['category_id'] is not None:
            category = Category.query.get(data['category_id'])
            if not category:
                return jsonify({"error": "Category not found"}), 404
        
        # Update allowed fields
        updateable_fields = ['title', 'description', 'category_id', 'publisher_id', 'star_rating']
        for field in updateable_fields:
            if field in data:
                setattr(game, field, data[field])
        
        # Commit changes
        db.session.commit()
        
        # Return updated game with full details
        updated_game = get_games_base_query().filter(Game.id == game.id).first()
        return jsonify(updated_game.to_dict()), 200
        
    except ValueError as e:
        # Handle validation errors from model validators
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except IntegrityError as e:
        # Handle database integrity errors
        db.session.rollback()
        return jsonify({"error": "Database integrity error"}), 400
    except Exception as e:
        # Handle unexpected errors
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500
@games_bp.route('/api/games/<int:id>', methods=['DELETE'])
def delete_game(id: int) -> tuple[Response, int]:
    """Delete an existing game"""
    try:
        # Find the game to delete
        game = Game.query.get(id)
        if not game:
            return jsonify({"error": "Game not found"}), 404
        
        # Delete the game
        db.session.delete(game)
        db.session.commit()
        
        # Return success message
        return jsonify({"message": "Game deleted successfully"}), 200
        
    except Exception as e:
        # Handle unexpected errors
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500
