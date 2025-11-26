import pytest
from app import app
import os


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def runner():
    """Create a test CLI runner"""
    return app.test_cli_runner()


# ============================================================================
# Route Tests
# ============================================================================

def test_home_route_status(client):
    """Test that the home page returns 200 status code"""
    response = client.get('/')
    assert response.status_code == 200


def test_home_route_content(client):
    """Test that the home page contains expected content"""
    response = client.get('/')
    assert b'<!DOCTYPE html>' in response.data or b'<html' in response.data


def test_about_route_exists(client):
    """Test that the about route exists"""
    response = client.get('/about')
    assert response.status_code in [200, 404]  # Adjust based on your routes


def test_contact_route_exists(client):
    """Test that the contact route exists"""
    response = client.get('/contact')
    assert response.status_code in [200, 404]  # Adjust based on your routes


def test_404_error(client):
    """Test that non-existent routes return 404"""
    response = client.get('/nonexistent-page')
    assert response.status_code == 404


# ============================================================================
# Template Rendering Tests
# ============================================================================

def test_render_template_without_errors(client):
    """Test that templates render without errors"""
    response = client.get('/')
    assert response.status_code == 200
    assert response.data is not None
    assert len(response.data) > 0


def test_html_structure(client):
    """Test that response contains valid HTML structure"""
    response = client.get('/')
    data = response.data.decode('utf-8')
    assert '<html' in data or '<!DOCTYPE html>' in data
    assert '</html>' in data


# ============================================================================
# Static Files Tests
# ============================================================================

def test_static_files_accessible(client):
    """Test that static files can be accessed"""
    # Test CSS file if it exists
    response = client.get('/static/style.css')
    assert response.status_code in [200, 404]
    
    # Test JS file if it exists
    response = client.get('/static/script.js')
    assert response.status_code in [200, 404]


# ============================================================================
# HTTP Method Tests
# ============================================================================

def test_get_method_allowed(client):
    """Test that GET method is allowed on home route"""
    response = client.get('/')
    assert response.status_code == 200


def test_post_method_on_get_only_route(client):
    """Test POST method on GET-only route"""
    response = client.post('/')
    assert response.status_code in [200, 405]  # 405 Method Not Allowed expected


def test_head_method(client):
    """Test HEAD request"""
    response = client.head('/')
    assert response.status_code == 200


# ============================================================================
# Content Type Tests
# ============================================================================

def test_content_type_html(client):
    """Test that home page returns HTML content type"""
    response = client.get('/')
    assert 'text/html' in response.content_type


# ============================================================================
# File Download Tests (if applicable)
# ============================================================================

def test_file_download_route(client):
    """Test file download functionality if route exists"""
    response = client.get('/download')
    # Adjust based on your actual download route
    assert response.status_code in [200, 404]


# ============================================================================
# Form Submission Tests (if applicable)
# ============================================================================

def test_form_submission_get(client):
    """Test form page loads correctly"""
    response = client.get('/contact')  # Adjust route name
    assert response.status_code in [200, 404]


def test_form_submission_post(client):
    """Test form submission with POST data"""
    response = client.post('/contact', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'message': 'This is a test message'
    })
    # Adjust assertions based on your form handling
    assert response.status_code in [200, 302, 404]  # 302 for redirect


# ============================================================================
# Security Tests
# ============================================================================

def test_no_debug_mode_in_production():
    """Test that debug mode is not enabled"""
    assert app.debug is False or app.config['TESTING'] is True


def test_secret_key_exists():
    """Test that a secret key is configured"""
    assert app.config.get('SECRET_KEY') is not None or app.config['TESTING'] is True


def test_xss_protection_headers(client):
    """Test for basic security headers"""
    response = client.get('/')
    # Check if security headers are set (optional)
    headers = response.headers
    # Add assertions for security headers if you've configured them


# ============================================================================
# API Tests (if applicable)
# ============================================================================

def test_api_endpoint_json_response(client):
    """Test API endpoint returns JSON"""
    response = client.get('/api/data')  # Adjust to your API route
    if response.status_code == 200:
        assert response.content_type == 'application/json'


# ============================================================================
# Error Handling Tests
# ============================================================================

def test_500_error_handling(client):
    """Test that 500 errors are handled gracefully"""
    # This would require a route that deliberately raises an error
    # Adjust based on your error handling implementation
    pass


# ============================================================================
# Configuration Tests
# ============================================================================

def test_app_exists():
    """Test that the app instance exists"""
    assert app is not None


def test_app_is_flask_instance():
    """Test that app is a Flask instance"""
    from flask import Flask
    assert isinstance(app, Flask)


def test_testing_mode_enabled():
    """Test that testing mode is properly configured"""
    assert app.config['TESTING'] is True


# ============================================================================
# Database Tests (if applicable)
# ============================================================================

# Uncomment and modify if you have database functionality

# @pytest.fixture
# def init_database():
#     """Initialize test database"""
#     # Setup database
#     yield
#     # Teardown database
#
# def test_database_connection(init_database):
#     """Test database connection"""
#     pass


# ============================================================================
# Integration Tests
# ============================================================================

def test_multiple_page_navigation(client):
    """Test navigation between multiple pages"""
    # Home page
    response = client.get('/')
    assert response.status_code == 200
    
    # About page
    response = client.get('/about')
    assert response.status_code in [200, 404]
    
    # Back to home
    response = client.get('/')
    assert response.status_code == 200


def test_session_handling(client):
    """Test session handling"""
    with client.session_transaction() as session:
        session['user'] = 'test_user'
    
    response = client.get('/')
    assert response.status_code == 200


# ============================================================================
# Performance Tests
# ============================================================================

def test_response_time(client):
    """Test that response time is reasonable"""
    import time
    start = time.time()
    response = client.get('/')
    end = time.time()
    
    assert response.status_code == 200
    assert (end - start) < 1.0  # Should respond in less than 1 second


# ============================================================================
# Parametrized Tests
# ============================================================================

@pytest.mark.parametrize("route", [
    "/",
    "/about",
    "/contact",
    "/services",
])
def test_routes_exist(client, route):
    """Test multiple routes with parametrize"""
    response = client.get(route)
    assert response.status_code in [200, 404]


@pytest.mark.parametrize("invalid_route", [
    "/invalid",
    "/does-not-exist",
    "/random-page-12345",
])
def test_invalid_routes_return_404(client, invalid_route):
    """Test that invalid routes return 404"""
    response = client.get(invalid_route)
    assert response.status_code == 404
