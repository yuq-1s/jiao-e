<!DOCTYPE html>
<html>
<head>
	<title>选课数据共享平台</title>
	<meta charset="utf-8">
	<meta meta name="viewport" content="width=device-width, initial-scale=1.0">
      <link href="http://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<?php
    //获取课程总数
	header("Content-Type: text/html; charset=utf-8");
	$conn=mysql_connect("localhost:3306","root");
	mysql_select_db("XUANKE") or die(mysql_error());
	mysql_query("SET NAMES 'utf8'",$conn);
	$sql1="SELECT COUNT(*) FROM Courses";
	$result1=mysql_query($sql1,$conn) or die(mysql_error());
	$row1=mysql_fetch_array($result1);
	$count1=$row1[0];
	//计算课程页数
	$pagesize=15;
	$totalpage=ceil($count1 / $pagesize);
	if(isset($_GET['page']) && $_GET['page'] > 0 && $_GET['page'] <= $totalpage){
		$page=$_GET['page'];
	}
	else $page=1;
	$start=($page-1)*$pagesize;
	//获取课程详细信息
	$sql2="SELECT * FROM Courses ORDER BY cid DESC LIMIT $start,$pagesize";
	$result2=mysql_query($sql2,$conn) or die(mysql_error());

	//与ajax相连接
	if($_POST){
		header("Content-type: text/html; charset=UTF-8");
		$data = $_POST['data'];
	$r = json_decode($data, true);
	foreach ($r as $value) {
   		$bsid = addslashes ($value['bsid']);
   		$now_number = addslashes ($value['now_number']);
   		$sql3 = "UPDATE Courses".
   				"SET now_number=$now_number".
   				"WHERE bsid=$bsid;";
   		mysql_query($sql3,$conn) or die(mysql_error());
	}
   }
?>
<div class="container">
	<div class="row clearfix">
		<div class="col-md-12 column">
			<nav class="navbar navbar-default" role="navigation">
				<div class="navbar-header">
					 <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1"> <span class="sr-only">Toggle navigation</span><span class="icon-bar"></span><span class="icon-bar"></span><span class="icon-bar"></span></button> <a class="navbar-brand" href="#">选课数据共享平台</a>
				</div>
				<div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
					<ul class="nav navbar-nav navbar-right">
						<li>
							 <a href="#">注册</a>
						</li>
						<li>
							 <a href="#">登录</a>
						</li>
						<li class="dropdown">
							 <a href="#" class="dropdown-toggle" data-toggle="dropdown">帮助<strong class="caret"></strong></a>
							<ul class="dropdown-menu">
								<li>
									 <a href="#">问题反馈</a>
								</li>
								<li>
									 <a href="#">联系我们</a>
								</li>
							</ul>
						</li>
					</ul>
				</div>
			</nav>
			<div class="tabbable" id="tabs-261818">
				<ul class="nav nav-tabs">
					<li class="active">
						 <a href="#panel-1" data-toggle="tab">选择课程</a>
					</li>
					<li>
						 <a href="#panel-216255" data-toggle="tab">已关注课程</a>
					</li>
				</ul>
				<div class="tab-content">
					<div class="tab-pane active" id="panel-1">
						<ul class="nav nav-tabs">
						<li class="active">
						 	<a href="#panel-1_1" data-toggle="tab">人文</a>
						</li>
						<li>
						 	<a href="#panel-1_2" data-toggle="tab">社科</a>
						</li>
						<li>
							 <a href="#panel-1_3" data-toggle="tab">自科</a>
						</li>
						<li>
							 <a href="#panel-1_4" data-toggle="tab">通选</a>
						</li>
						</ul>
						<table class="table table-striped table-bordered table-hover table-condensed">
							<thead>
								<tr>
								<th>课程代号</th>
								<th>授课教师</th>
								<th>满课人数</th>
								<th>现有人数</th>
								<th>关注课程</th>
								</tr>
							</thead>
							<tbody>
								<?php
								while($row2=mysql_fetch_array($result2) ){?>
									<tr>
										<td><?php echo $row2['cid'] ?></td>
										<td><?php echo $row2['teacher'] ?></td>
										<td><?php echo $row2['max_number']?></td>
										<td><?php echo $row2['now_number'] ?></td>
										<td><button class="btn btn-default">关注</button></td>
									</tr>
								<?php }?>
							</tbody>
							
						</table>
					<ul class="pagination" style="text-align:center">
					   <li><a><?php if($totalpage!=0) echo $page. "/" .$totalpage;
                         else echo "暂无课程"; ?></a></li>
					   
				       <li><?php if($page==1 || $page > $totalpage) {?><a >首页</a>
					   <?php } else {?><a href="index.php?location=2&&page=1">首页</a><?php }?>
					   </li>
					   <li><?php if($page==1 || $page > $totalpage) {?><a >上一页</a>
					   <?php } else {?><a href="index.php?location=2&&page=<?php echo $page-1 ?>">上一页</a><?php }?>
					   </li>
					   <li><?php if($page==$totalpage || $page > $totalpage) { ?><a >下一页</a>
					   <?php } else {?><a href="index.php?location=2&&page=<?php echo $page+1 ?>">下一页</a><?php }?>
					   </li>
					   <li><?php if($page==$totalpage || $page > $totalpage) { ?><a >尾页</a>
					   <?php } else {?><a href="index.php?location=2&&page=<?php echo $totalpage ?>">尾页</a><?php }?>
					   </li>
					</ul>
					</div>
					<div class="tab-pane" id="panel-216255">
						<table class="table table-striped table-bordered table-hover table-condensed">
							<thead>
								<tr>
								<th>课程代号</th>
								<th>课程名称</th>
								<th>课程人数</th>
								<th>取消关注</th>
								</tr>
								</thead>
							<tbody>
								<tr>
								<td></td>
								<td></td>
								<td></td>
								<td><button class="btn btn-default">取消</button></td>
								</tr>
								<tr>
								<td></td>
								<td></td>
								<td></td>
								<td><button class="btn btn-default">取消</button></td>
								</tr>
								<tr>
								<td></td>
								<td></td>
								<td></td>
								<td><button class="btn btn-default">取消</button></td>
								</tr>
								</tbody>

						</table>
						<ul class="pagination" style="text-align:center">
					   <li><a><?php if($totalpage!=0) echo $page. "/" .$totalpage;
                         else echo "暂无课程"; ?></a></li>
					   
				       <li><?php if($page==1 || $page > $totalpage) {?><a >首页</a>
					   <?php } else {?><a href="index.php?location=2&&page=1">首页</a><?php }?>
					   </li>
					   <li><?php if($page==1 || $page > $totalpage) {?><a >上一页</a>
					   <?php } else {?><a href="index.php?location=2&&page=<?php echo $page-1 ?>">上一页</a><?php }?>
					   </li>
					   <li><?php if($page==$totalpage || $page > $totalpage) { ?><a >下一页</a>
					   <?php } else {?><a href="index.php?location=2&&page=<?php echo $page+1 ?>">下一页</a><?php }?>
					   </li>
					   <li><?php if($page==$totalpage || $page > $totalpage) { ?><a >尾页</a>
					   <?php } else {?><a href="index.php?location=2&&page=<?php echo $totalpage ?>">尾页</a><?php }?>
					   </li>
					</ul>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
<div class="navbar" style="background-image:url(./group/1/multi/bgi.jpg);">
	  <div class="navbar-inner">
	      <p style="text-align:center">版权@选课数据共享平台</p>
	  </div>
</div>
<script src="http://cdn.bootcss.com/jquery/3.0.0/jquery.min.js"></script>
<script src="http://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</body>
</html>