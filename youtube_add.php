<?php
$file = 'youtube.txt';
// Open the file to get existing content

// Append a new person to the file
$current = $_GET["vid"];
// Write the contents back to the file

$code_get = $_GET["code"];
// Write the contents back to the file
//file_put_contents($file, $current);

$code_md5=md5($current. "??????");

//echo "</br>"."add vid:" . $current."</br>";
//echo "</br>"."input code =".$code_get."</br>";
//echo "</br>"."MD5('".$current."??????')=".$code_md5."</br></br></br>";

if ($code_get== $code_md5)
{
file_put_contents($file, $current);
echo "add vid:" . $current;
}

else
{
echo "Fail to check the code" ;
}

?>
