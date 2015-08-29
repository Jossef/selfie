<?php 
	$files = scandir(dirname(__FILE__));
	$output = array();
	foreach ($files as $file)
	  if (!in_array($file, array(".", "..", "index.php", ".htaccess")))
	    $output[] = $file;
	header("Content-type: text/json");
	echo json_encode($output);
?> 