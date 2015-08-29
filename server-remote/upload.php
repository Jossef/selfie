<?php 
	$target_path = "uploads/" . basename( $_FILES['file']['name']); 

	if(move_uploaded_file($_FILES['file']['tmp_name'], $target_path)) { 
	    echo "The file has been uploaded successfully";
	    echo '<script type="text/javascript">window.location = "http://jossef.com/selfie/thanks.html";</script>';
	} else{
	    header('There was an error uploading the file!', true, 500);
		print_r($_FILES);
	}
?> 