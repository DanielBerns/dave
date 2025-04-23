import os
from flask import request, jsonify, current_app, abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.api import bp
from app.models import User, TextHTML, Image
from app import db

def allowed_file(filename: str) -> bool:
    """Checks if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/text_html_set', methods=['GET'])
@login_required # Protect API endpoint
def get_resources():
    """Returns a list of resources accessible to the user."""
    # Basic implementation: return all resources by the current user
    # Add pagination, filtering, searching as needed
    user_text_htmls = DBOps.look_for_text_html(author=current_user)
    uth_list = [uth.to_dict() for uth in user_text_htmls]
    return jsonify(uth_list)

@bp.route('/resources/<int:resource_id>', methods=['GET'])
@login_required
def get_resource(resource_id: int):
    """Returns details of a specific resource."""
    resource = Resource.query.get_or_404(resource_id)
    # Ensure the user owns the resource or has permission (implement logic if needed)
    if resource.user_id != current_user.id:
         abort(403) # Forbidden

    resource_data = {
        'id': resource.id,
        'name': resource.name,
        'type': resource.resource_type.name,
        'timestamp': resource.timestamp.isoformat(),
        'author_id': resource.user_id,
        'filepath': resource.filepath if resource.resource_type == ResourceType.IMAGE else None,
        'html_content': resource.html_content if resource.resource_type == ResourceType.HTML else None,
    }
    return jsonify(resource_data)


@bp.route('/resources/upload', methods=['POST'])
@login_required
def upload_resource():
    """Uploads a new resource (HTML content or image file)."""
    resource_type_str = request.form.get('type')
    resource_name = request.form.get('name')

    if not resource_type_str or not resource_name:
        return jsonify({'error': 'Missing resource type or name'}), 400

    try:
        resource_type = ResourceType(resource_type_str.lower())
    except ValueError:
        return jsonify({'error': f'Invalid resource type: {resource_type_str}. Must be "html" or "image".'}), 400

    new_resource = Resource(
        name=resource_name,
        resource_type=resource_type,
        author=current_user # Associate with the logged-in user
    )

    if resource_type == ResourceType.HTML:
        html_content = request.form.get('html_content')
        if not html_content:
            return jsonify({'error': 'Missing html_content for HTML resource'}), 400
        new_resource.html_content = html_content

    elif resource_type == ResourceType.IMAGE:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename) # Sanitize filename
            # Ensure unique filenames to avoid overwrites (e.g., add timestamp or UUID)
            # For simplicity, we use the original secure name here
            save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

            # Check if file already exists (optional, decide on overwrite policy)
            if os.path.exists(save_path):
                 # Option 1: Error out
                 # return jsonify({'error': f'File "{filename}" already exists.'}), 409 # Conflict
                 # Option 2: Generate unique name (e.g., append timestamp/uuid)
                 base, ext = os.path.splitext(filename)
                 filename = f"{base}_{int(datetime.utcnow().timestamp())}{ext}"
                 save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)


            try:
                file.save(save_path)
                new_resource.filepath = filename # Store relative path/filename
            except Exception as e:
                # Log the exception e
                db.session.rollback() # Rollback if file save fails after starting DB transaction
                return jsonify({'error': f'Failed to save file: {str(e)}'}), 500
        else:
            return jsonify({'error': 'File type not allowed'}), 400
    else:
         # Should not happen due to enum check, but good practice
         return jsonify({'error': 'Unsupported resource type specified'}), 400


    try:
        db.session.add(new_resource)
        db.session.commit()
        # Return the created resource info
        resource_data = {
            'id': new_resource.id,
            'name': new_resource.name,
            'type': new_resource.resource_type.name,
            'timestamp': new_resource.timestamp.isoformat(),
            'author_id': new_resource.user_id,
            'filepath': new_resource.filepath if new_resource.resource_type == ResourceType.IMAGE else None,
        }
        return jsonify({'message': 'Resource uploaded successfully', 'resource': resource_data}), 201
    except Exception as e:
        db.session.rollback()
        # Log the exception e
        # Clean up saved file if DB commit fails
        if resource_type == ResourceType.IMAGE and 'save_path' in locals() and os.path.exists(save_path):
             try:
                 os.remove(save_path)
             except OSError:
                 pass # Log failure to remove file
        return jsonify({'error': f'Database error: {str(e)}'}), 500


@bp.route('/resources/<int:resource_id>', methods=['DELETE'])
@login_required
def delete_resource(resource_id):
    """Deletes a resource."""
    resource = Resource.query.get_or_404(resource_id)

    # Ensure the current user owns the resource
    if resource.user_id != current_user.id:
        abort(403) # Forbidden

    try:
        # If it's an image, delete the associated file
        if resource.resource_type == ResourceType.IMAGE and resource.filepath:
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], resource.filepath)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except OSError as e:
                    # Log the error but proceed with DB deletion? Or abort?
                    # For now, log and continue.
                    current_app.logger.error(f"Error deleting file {file_path}: {e}")


        db.session.delete(resource)
        db.session.commit()
        return jsonify({'message': f'Resource {resource_id} deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting resource {resource_id}: {e}")
        return jsonify({'error': f'Failed to delete resource: {str(e)}'}), 500

# Add PUT/PATCH endpoint for updating resources as needed


# The `api` blueprint provides endpoints for managing resources.
# It includes routes to list resources (`GET /resources`), get a specific resource (`GET /resources/<id>`),
# upload a new resource (`POST /resources/upload`), and delete a resource (`DELETE /resources/<id>`).
# These endpoints are protected using `@login_required` and include basic validation and error handling.
# Image uploads are saved to the configured UPLOAD_FOLDER
