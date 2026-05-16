#!/usr/bin/env python3
"""
Script to create feature issues for the extracurricular activities management system
"""

import requests
import json
import sys

# Configuration
OWNER = "IgarKh"
REPO = "skills-integrate-mcp-with-copilot"
GITHUB_TOKEN = input("Enter your GitHub personal access token: ").strip()

if not GITHUB_TOKEN:
    print("GitHub token is required!")
    sys.exit(1)

# GitHub API endpoint
ISSUES_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/issues"

# Headers for authentication
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Issues to create
issues = [
    {
        "title": "Add comprehensive member management system",
        "body": """Implement full CRUD operations for member profiles including:
- Personal information (first name, last name, DOB)
- Contact details (email, phone number)
- Address information (building, street, city)
- Membership type assignment
- Status tracking (Active/Inactive/Suspended)
- Membership start/end dates

This should include database models, API endpoints, and UI components.""",
        "labels": ["feature", "members", "database"]
    },
    {
        "title": "Add trainer and staff management functionality",
        "body": """Create a system to manage trainers/instructors with:
- Staff profiles (name, email, phone, hire date)
- Specialization tracking (Yoga, Swimming, Boxing, etc.)
- Employment status management
- Full CRUD operations

Include database models, API endpoints, and management interface.""",
        "labels": ["feature", "staff", "database"]
    },
    {
        "title": "Implement facility resource management",
        "body": """Build facility management with:
- Multiple facility types (Pool, Gym, Court)
- Facility capacity tracking
- Location/address information
- Status management (Available/Under Maintenance/Closed)
- Full CRUD operations

Include database design and API endpoints.""",
        "labels": ["feature", "facilities", "database"]
    },
    {
        "title": "Enhance activity management with difficulty levels and fees",
        "body": """Extend activity system with:
- Difficulty levels (Beginner/Intermediate/Advanced)
- Per-activity fee tracking
- Activity capacity management
- Activity status control
- Complete activity descriptions

This enhances the existing activity endpoints and data model.""",
        "labels": ["feature", "activities", "enhancement"]
    },
    {
        "title": "Add activity scheduling with time slots and recurring patterns",
        "body": """Implement comprehensive scheduling:
- Link activities to specific facilities
- Assign trainers to scheduled sessions
- Date range and time slot specifications
- Recurring schedule support (by day of week)
- Schedule management operations (CRUD)

Include database models and API endpoints.""",
        "labels": ["feature", "scheduling", "database"]
    },
    {
        "title": "Add facility booking and reservation system",
        "body": """Create member-based facility reservations:
- Reserve facilities by date and time slot
- Reservation status tracking (Pending/Confirmed/Cancelled/Completed)
- Prevent double-booking
- Manage facility availability

Include database schema and API endpoints for reservation management.""",
        "labels": ["feature", "reservations", "database"]
    },
    {
        "title": "Improve activity participation with multiple states",
        "body": """Extend participation tracking to include:
- Multiple states (Enrolled/Completed/Dropped/Waitlisted)
- Prevent duplicate enrollments
- Enrollment date recording
- Activity completion tracking

Enhance the existing signup/participation system.""",
        "labels": ["feature", "participation", "enhancement"]
    },
    {
        "title": "Migrate from in-memory storage to persistent database",
        "body": """Replace in-memory activity storage with:
- Relational database (PostgreSQL or similar)
- Proper schema design with foreign keys
- Transaction support
- Data persistence across sessions

This is a critical infrastructure upgrade for production readiness.""",
        "labels": ["feature", "database", "infrastructure"]
    },
    {
        "title": "Create administrative dashboard interface",
        "body": """Build a comprehensive admin dashboard featuring:
- System overview and key metrics
- Quick access to all management functions
- Statistics and reporting
- Centralized management interface

Include both backend and frontend components.""",
        "labels": ["feature", "UI/UX", "frontend"]
    },
    {
        "title": "Implement transaction support and referential integrity",
        "body": """Add database-level protections:
- Transaction support for complex multi-step operations
- Referential integrity constraints
- Cascade/set null delete/update rules
- Data validation with check constraints

Ensures data consistency and reliability.""",
        "labels": ["feature", "database", "reliability"]
    }
]

print(f"Creating {len(issues)} issues in {OWNER}/{REPO}...\n")

created_count = 0
failed_count = 0

for i, issue in enumerate(issues, 1):
    data = {
        "title": issue["title"],
        "body": issue["body"],
        "labels": issue["labels"]
    }
    
    try:
        response = requests.post(ISSUES_URL, json=data, headers=headers)
        
        if response.status_code == 201:
            issue_num = response.json()["number"]
            print(f"✓ Issue #{issue_num}: {issue['title']}")
            created_count += 1
        else:
            print(f"✗ Failed to create: {issue['title']}")
            print(f"  Error: {response.status_code} - {response.json().get('message', 'Unknown error')}\n")
            failed_count += 1
    except Exception as e:
        print(f"✗ Exception creating: {issue['title']}")
        print(f"  Error: {str(e)}\n")
        failed_count += 1

print(f"\n{'='*60}")
print(f"Summary: {created_count} created, {failed_count} failed")
print(f"{'='*60}")
