def test_pagina_de_usuario_retorna_200(test_client):

    response = test_client.get('/')
    assert response.status_code == 200