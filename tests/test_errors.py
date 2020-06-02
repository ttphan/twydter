def test_404(client, session):
    response = client.get('/totallynonsensicallink')
    assert response.status_code == 404
    assert b'Page Not Found' in response.data
