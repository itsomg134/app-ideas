<?php
session_start();

// Initialize tasks array in session if not exists
if (!isset($_SESSION['tasks'])) {
    $_SESSION['tasks'] = [];
}

// Handle form submissions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_POST['action'])) {
        switch ($_POST['action']) {
            case 'add':
                if (!empty($_POST['task'])) {
                    $newTask = [
                        'id' => uniqid(),
                        'text' => htmlspecialchars($_POST['task']),
                        'completed' => false,
                        'created_at' => date('Y-m-d H:i:s')
                    ];
                    $_SESSION['tasks'][] = $newTask;
                }
                break;
            
            case 'toggle':
                if (isset($_POST['task_id'])) {
                    foreach ($_SESSION['tasks'] as &$task) {
                        if ($task['id'] === $_POST['task_id']) {
                            $task['completed'] = !$task['completed'];
                            break;
                        }
                    }
                }
                break;
            
            case 'delete':
                if (isset($_POST['task_id'])) {
                    $_SESSION['tasks'] = array_filter($_SESSION['tasks'], function($task) {
                        return $task['id'] !== $_POST['task_id'];
                    });
                    $_SESSION['tasks'] = array_values($_SESSION['tasks']);
                }
                break;
            
            case 'clear_completed':
                $_SESSION['tasks'] = array_filter($_SESSION['tasks'], function($task) {
                    return !$task['completed'];
                });
                $_SESSION['tasks'] = array_values($_SESSION['tasks']);
                break;
        }
    }
    header('Location: ' . $_SERVER['PHP_SELF']);
    exit;
}

$totalTasks = count($_SESSION['tasks']);
$completedTasks = count(array_filter($_SESSION['tasks'], function($task) {
    return $task['completed'];
}));
$pendingTasks = $totalTasks - $completedTasks;
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PHP Todo App</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            width: 100%;
            max-width: 600px;
            padding: 30px;
        }
        
        h1 {
            color: #667eea;
            margin-bottom: 10px;
            text-align: center;
        }
        
        .stats {
            display: flex;
            justify-content: space-around;
            margin-bottom: 25px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        
        .stat {
            text-align: center;
        }
        
        .stat-number {
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }
        
        .stat-label {
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
        }
        
        .add-task-form {
            display: flex;
            gap: 10px;
            margin-bottom: 25px;
        }
        
        input[type="text"] {
            flex: 1;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }
        
        button {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .btn-primary {
            background: #667eea;
            color: white;
        }
        
        .btn-primary:hover {
            background: #5568d3;
            transform: translateY(-2px);
        }
        
        .btn-danger {
            background: #ff6b6b;
            color: white;
            padding: 8px 16px;
            font-size: 14px;
        }
        
        .btn-danger:hover {
            background: #ee5a52;
        }
        
        .btn-clear {
            background: #f8f9fa;
            color: #666;
            width: 100%;
            margin-top: 15px;
        }
        
        .btn-clear:hover {
            background: #e9ecef;
        }
        
        .tasks-list {
            list-style: none;
        }
        
        .task-item {
            display: flex;
            align-items: center;
            padding: 15px;
            margin-bottom: 10px;
            background: #f8f9fa;
            border-radius: 8px;
            transition: all 0.3s;
        }
        
        .task-item:hover {
            transform: translateX(5px);
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .task-item.completed {
            opacity: 0.6;
        }
        
        .task-checkbox {
            margin-right: 15px;
        }
        
        input[type="checkbox"] {
            width: 20px;
            height: 20px;
            cursor: pointer;
        }
        
        .task-text {
            flex: 1;
            font-size: 16px;
            color: #333;
        }
        
        .task-item.completed .task-text {
            text-decoration: line-through;
            color: #999;
        }
        
        .task-time {
            font-size: 12px;
            color: #999;
            margin-right: 15px;
        }
        
        .empty-state {
            text-align: center;
            padding: 40px;
            color: #999;
        }
        
        .empty-state svg {
            width: 80px;
            height: 80px;
            margin-bottom: 15px;
            opacity: 0.5;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📝 My Todo List</h1>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-number"><?php echo $totalTasks; ?></div>
                <div class="stat-label">Total</div>
            </div>
            <div class="stat">
                <div class="stat-number"><?php echo $pendingTasks; ?></div>
                <div class="stat-label">Pending</div>
            </div>
            <div class="stat">
                <div class="stat-number"><?php echo $completedTasks; ?></div>
                <div class="stat-label">Completed</div>
            </div>
        </div>
        
        <form method="POST" class="add-task-form">
            <input type="hidden" name="action" value="add">
            <input type="text" name="task" placeholder="What needs to be done?" required>
            <button type="submit" class="btn-primary">Add Task</button>
        </form>
        
        <?php if (empty($_SESSION['tasks'])): ?>
            <div class="empty-state">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path>
                </svg>
                <p>No tasks yet. Add one above to get started!</p>
            </div>
        <?php else: ?>
            <ul class="tasks-list">
                <?php foreach ($_SESSION['tasks'] as $task): ?>
                    <li class="task-item <?php echo $task['completed'] ? 'completed' : ''; ?>">
                        <form method="POST" class="task-checkbox">
                            <input type="hidden" name="action" value="toggle">
                            <input type="hidden" name="task_id" value="<?php echo $task['id']; ?>">
                            <input type="checkbox" 
                                   <?php echo $task['completed'] ? 'checked' : ''; ?>
                                   onchange="this.form.submit()">
                        </form>
                        
                        <span class="task-text"><?php echo $task['text']; ?></span>
                        <span class="task-time"><?php echo date('M j, g:i A', strtotime($task['created_at'])); ?></span>
                        
                        <form method="POST" style="display: inline;">
                            <input type="hidden" name="action" value="delete">
                            <input type="hidden" name="task_id" value="<?php echo $task['id']; ?>">
                            <button type="submit" class="btn-danger">Delete</button>
                        </form>
                    </li>
                <?php endforeach; ?>
            </ul>
            
            <?php if ($completedTasks > 0): ?>
                <form method="POST">
                    <input type="hidden" name="action" value="clear_completed">
                    <button type="submit" class="btn-clear">Clear Completed Tasks</button>
                </form>
            <?php endif; ?>
        <?php endif; ?>
    </div>
</body>
</html>
