from errors.keycloak_errors import BadCredentialsError, GroupUnauthorizedKeycloakError, KeycloakUnauthorizedError


def test_bad_credentials_error():
    try:
        raise BadCredentialsError('Bad credentials')
    except BadCredentialsError as e:
        assert str(e) == 'Bad credentials'


def test_group_unauthorized_keycloak_error():
    try:
        raise GroupUnauthorizedKeycloakError('user admin')
    except GroupUnauthorizedKeycloakError as e:
        assert str(e) == 'Unauthorized, authorized group: user admin'


def test_unauthorized_keycloak_error():
    try:
        raise KeycloakUnauthorizedError('Unauthorized')
    except KeycloakUnauthorizedError as e:
        assert str(e) == 'Unauthorized'
