<!DOCTYPE html>
<html>
<meta charset="utf-8">
<meta meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="http://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
<head>
	<title>注册</title>
</head>
<body>
<?php
	if(isset($_POST['add']))
	{
		$dbhost = 'localhost:3306';
		$dbuser = 'root';
		$dbpass = '';
		$conn = mysql_connect($dbhost,$dbuser,$dbpass);
		if(!$conn)
		{
			die('Could not connect:'.mysql_error());
		}
		if(!get_magic_quotes_gpc())
		{
			$user_name = addslashes($_POST['user_name']);
			$password = addslashes($_POST['password']);
			$email_address = addslashes($_POST['email_address']);
		}
		else
		{
			$user_name = $_POST['username'];
			$password = $_POST['password'];
			$email_address = $_POST['email_address'];
		}
		$sql = "INSERT INTO users".
				"(user_name,password,email_address)".
				"VALUES".
				"('$user_name','$password','$email_address');";
		mysql_select_db('XUANKE');
		$retval = mysql_query($sql,$conn);
		if(!$retval)
		{
			die("Could not enter data:".mysql_error());
		}
		echo "Entered data successfully!\n";
		mysql_close($conn);
	}
	else
	{
 ?>
<form role="form" method="post" action="<?php $_PHP_SELF ?>">
	<div class="form-group">
		<label for="user_name">用户名</label><input type="text" class="form-control" id="user_name" name="user_name"/>
	</div>
	<div class="form-group">
		<label for="email_address">注册邮箱地址</label><input type="email" class="form-control" id="email_address" name="email_address"/>
	</div>
	<div class="form-group">
		<label for="password">注册密码</label><input type="password" class="form-control" id="password" name="password"/>
	</div>
	<div class="checkbox">
		 <label><input type="checkbox" />已确认</label>
	</div> 
	<button type="submit" class="btn btn-default" id="add" name="add">提交</button>
</form>
 <?php 
	}
  ?>
<script src="http://cdn.bootcss.com/jquery/3.0.0/jquery.min.js"></script>
<script src="http://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</body>
</html>