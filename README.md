### Feature

- [x] di chuyen the giua cac column
- [x] tao, xoa cot
- [x] tao, xoa the

#### 1. User
- [x] `Sign up`, `sign in`, `sign out` with email and password
### Database Design

#### Table: `users`

| Column Name | Data Type | Details |
|-------------|-----------|---------|
| id          | integer   | not null, primary key |
| username    | string    | not null, unique |
| email       | string    | not null, unique |
| password    | string    | not null |

#### Table: `profiles`

| Column Name  | Data Type   | Details |
|--------------|-------------|---------|
| id           | integer     | not null, primary key, foreign key (references users) |
| name         | string    | not null |
| profile_pic  | string      | not null |
| workspace_owner_orders | json(str[]) | not null |
| workspace_member_orders | json(str[]) | not null |

#### Table: `workspaces`

| Column Name | Data Type | Details |
|-------------|-----------|---------|
| id          | integer   | not null, primary key |
| name        | string    | not null |
| icon_unified | string    | not null |
| column_orders | json(str[]) | not null |
| created_at  | datetime  | not null |

### Table: `columns`

> **Note**: `type` field

| Column Name | Data Type | Details |
|-------------|-----------|---------|
| id          | integer   | not null, primary key |
| workspace_id | integer   | not null, foreign key (references workspaces) |
| name        | string    | not null |
| card_orders | json(str[]) | not null |
<!-- | type       | string('todo', 'doing', 'done', 'none') | not null | -->

### Table: `cards`

| Column Name | Data Type | Details |
|-------------|-----------|---------|
| id          | integer   | not null, primary key |
| column_id   | integer   | not null, foreign key (references columns) |
| content     | string    | not null |
| due_date    | datetime  | not null |
| assignee_id | integer   | not null, foreign key (references users) |

### Table: `tasks`

> **Note**: `Ordering` by `create_at` field

| Column Name | Data Type | Details |
|-------------|-----------|---------|
| id          | integer   | not null, primary key |
| card_id     | integer   | not null, foreign key (references cards) |
| content     | string    | not null |
| status      | string('todo', 'progress', 'done') | not null |

#### Table: `users_workspaces`

| Column Name | Data Type | Details |
|-------------|-----------|---------|
| id          | integer   | not null, primary key |
| user_id     | integer   | not null, foreign key (references profile) |
| workspace_id| integer   | not null, foreign key (references workspaces) |
| role        | string('owner', 'member') | not null |

### Table: 'workspace_logs'

| Column Name | Data Type | Details |
|-------------|-----------|---------|
| id          | integer   | not null, primary key |
| workspace_id| integer   | not null, foreign key (references workspaces) |
| log        | string    | not null |
| created_at  | datetime  | not null |

### Table: `notifications`

> Notifications được tạo khi user được assign vào task

| Column Name | Data Type | Details |
|-------------|-----------|---------|
| id          | integer   | not null, primary key |
| user_id     | integer   | not null, foreign key (references profile) | # User nhận notification
| workspace_id| integer   | not null, foreign key (references workspaces) | # Workspace liên quan
| message     | string    | not null | # Tran Dinh Van đã assign bạn vào task
| created_at  | datetime  | not null |

### Table: `requests`

> Requests được tạo khi mời user vào workspace

| Column Name | Data Type | Details |
|-------------|-----------|---------|
| id          | integer   | not null, primary key |
| user_receive_id | integer | not null, foreign key (references profile) | # User nhận request
| workspace_id | integer | not null, foreign key (references workspaces) | # Workspace liên quan
| status       | string('pending', 'accepted', 'rejected') | not null |
| created_at   | datetime  | not null |


###