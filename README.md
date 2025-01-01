### Feature

#### Automation 

> **Note**: Automation có tác dụng giúp tự động hóa các công việc. Automation là một chuỗi các command. Mỗi command sẽ thực hiện một công việc nhất định.

`command-type`: `CREATE`, `MOVE`, `DELETE`

`command`: 

Mỗi command sẽ có một cấu trúc nhất định tuỳ theo `command-type`

> ex: CREATE:`name`:`due_date`:`assignee_id` 

> ex: MOVE:`$card_id`:`^column_id`:`$^column_id`

**Chi tiết các command**:
-   `CREATE`: Tạo một card mới
    
    > ex: CREATE:`name`:`short_desc`:`due_date`:`assignee_id`:`column_id`

    -   `name`: Tên của card
    -   `short_desc`: Mô tả ngắn gọn của card
    -   `due_date`: Ngày hết hạn của card
    -   `assignee_id`: ID của người được giao việc
    -   `column_id`: ID của column mà card sẽ được tạo

-   `MOVE`: Di chuyển card từ column này sang column khác

    > ex: MOVE:`$card_id`:`^column_id`:`$^column_id`

    -   `$card_id`: ID của card
    -   `^column_id`: ID của column mà card sẽ được di chuyển

-   `DELETE`: Xóa card

    > ex: DELETE:`$card_id`

    -   `$card_id`: ID của card

**Chaining command**: Các command sẽ được nối với nhau bằng dấu `;`

> ex: CREATE:`name`:`short_desc`:`due_date`:`assignee_id`:`column_id`;MOVE:`$card_id`:`^column_id`:`$^column_id`;DELETE:`$card_id`


### Database Design

#### Table: `Automation`

| Column Name | Data Type | Details |
|-------------|-----------|---------|
| id          | integer   | not null, primary key |
| workspace_id| integer   | not null, foreign key (references workspaces) |
| name        | string    | not null |
| command-type| string    | not null | # 'CREATE', 'MOVE', 'DELETE'
| command     | string    | not null |
| created_at  | datetime  | not null |

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