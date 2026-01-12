
def test_knowledge_search_filters(client, auth_headers):
    response_one = client.post(
        "/knowledge/",
        json={
            "title": "Reset MFA guide",
            "content": "Steps to reset MFA tokens.",
            "tags": ["Auth", "MFA"],
        },
        headers=auth_headers,
    )
    assert response_one.status_code == 201

    response_two = client.post(
        "/knowledge/",
        json={
            "title": "Incident comms template",
            "content": "How to draft incident updates.",
            "tags": ["Comms", "Incident"],
        },
        headers=auth_headers,
    )
    assert response_two.status_code == 201

    keyword_response = client.get("/knowledge/?keyword=MFA", headers=auth_headers)
    assert keyword_response.status_code == 200
    titles = [article["title"] for article in keyword_response.json()]
    assert "Reset MFA guide" in titles
    assert "Incident comms template" not in titles

    tag_response = client.get("/knowledge/?tags=incident", headers=auth_headers)
    assert tag_response.status_code == 200
    tag_titles = [article["title"] for article in tag_response.json()]
    assert "Incident comms template" in tag_titles
    assert "Reset MFA guide" not in tag_titles
