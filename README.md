# Login API – Sequence Diagram

```mermaid
	sequenceDiagram
	autonumber

		participant Client                as Client / Browser / cURL
		participant Router                as FastAPI\n`POST /api/v1/auth/login`
		participant LoginUseCase          as `LoginUseCase.execute()`
		participant AuthService           as `AuthService`
		participant UserRepo              as `UserRepository`
		participant DB                    as Database
		participant PasswordService       as `PasswordService`
		participant TokenService          as `TokenService`
		participant Security              as `core.security`

		Client  ->>  Router          : Form-encoded username & password
		Router  ->>  LoginUseCase    : `execute(username, password)`
		LoginUseCase  ->>  AuthService  : `validate_credentials()`

		%% --- Validate credentials ----------------------------
		AuthService   ->>  UserRepo   : `get_user_by_email_or_phone(username)`
		UserRepo      ->>  DB         : SQL SELECT user
		DB            -->> UserRepo   : user row
		UserRepo      -->> AuthService: `UserEntity`

		AuthService   ->>  PasswordService : `verify_password(hash, password)`
		PasswordService ->> Security  : `verify_password()`
		Security      -->> PasswordService : boolean
		PasswordService -->> AuthService   : boolean

		AuthService  -->>  LoginUseCase    : valid `UserEntity`
		%% --- Credentials validated ---------------------------

		%% --- Generate token ----------------------------------
		LoginUseCase  ->>  TokenService  : `generate_token(TokenPayload)`
		TokenService  ->>  Security      : `create_access_token(payload)`
		Security      -->> TokenService  : JWT access-token
		TokenService  -->> LoginUseCase  : token string
		%% ------------------------------------------------------

		LoginUseCase  -->>  Router       : `LoginResponseDTO(token, user)`
		Router        -->>  Client       : 200 OK\n`Response.success(...)`

```

### Viewing the Diagram

GitHub now supports rendering Mermaid diagrams natively. After pushing this README to GitHub (or viewing it in any Markdown viewer with Mermaid support, such as the VS Code "Markdown Preview Mermaid Support" extension), you will see the diagram rendered automatically.

If you are using a Markdown viewer that does **not** support Mermaid, the fenced code will simply appear as text. In that case you can:

1. Copy the fenced diagram code above and paste it into the [Mermaid Live Editor](https://mermaid.live/).
2. Export SVG/PNG from the live editor and embed it as an image instead.
