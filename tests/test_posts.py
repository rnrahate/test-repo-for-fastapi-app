from typing import List
from app import schemas
import pytest

def test_get_all_posts(authorize_client, test_posts):
    res = authorize_client.get("/posts/")
    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, res.json())
    print(list(posts_map))
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    print("Get all posts test passed!")

def test_unauthorized_get_all_posts(client,test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401
    print("Unauthorized access test passed!")

def test_unauthorized_get_single_post(client,test_posts):
    post_id = test_posts[0].id
    res = client.get(f"/posts/{post_id}")
    assert res.status_code == 401
    print("Unauthorized access to single post test passed!")

def test_get_single_post(authorize_client, test_posts):
    post_id = test_posts[0].id
    res = authorize_client.get(f"/posts/{post_id}")

    post = schemas.Post.model_validate(res.json())

    assert res.status_code == 200
    assert post.id == test_posts[0].id

def test_get_nonexistent_post(authorize_client):
    res = authorize_client.get("/posts/9999")
    assert res.status_code == 404
    print("Get non-existent post test passed!")

@pytest.mark.parametrize("title, content, published", [
    ("Test Title", "Test Content", True),
    ("Another Title", "Another Content", False),
    ("Third Title", "Third Content", True)
])
def test_create_post(authorize_client, title, content, published):
    res = authorize_client.post("/posts/", json={"title": title, "content": content, "published": published})
    created_post = schemas.Post.model_validate(res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    print("Create post test passed!")