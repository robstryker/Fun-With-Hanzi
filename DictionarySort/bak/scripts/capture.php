#!/usr/bin/php
<?php 
$o = getOpt("a:");
$c = $o["a"];

loadExamplesFor($c); 

function loadExamplesFor($char) {
   $r2 = trim(`cat count_hanzi`);
   $fnum = trim(`cat count_filename`);
   log2( "Starting $char - $r2");
   $i = 1;
   $needsMore = true;
   while( $needsMore ){
       getPage($char, $i);
       $needsMore = parseFileHasMoreExamples($char, $i);
       $cmd = 'cat file | grep "SPS.commonLayer.newTTS"  | ./clean.sh >> ../outputs/examples/' . $fnum . '.txt';
       $result = `$cmd`;
       $i++;
   } 
   `./increment.sh`;
   $x = substr($r2, -3); 
   if( substr($r2, -3) == "000")
     `./increment_filename.sh`;
}

function log2( $x ) {
   $logCmd = "echo \"$x\" >> log";
   `$logCmd`;
}

function getPage($char, $i) {
//   log2( "  $char : $i");
   $cmd = "wget -O file http://www.nciku.com/search/all/examples/" . $char . "?pageNo=" . $i;
   `$cmd`;
}

function parseFileHasMoreExamples($char, $i) {
   $result = trim(`cat file | grep "h3 class="`);
   $parenLoc = strpos($result, "-") + 1;
   $closeParen = strpos($result, ")");
   $result = substr($result, $parenLoc, $closeParen-$parenLoc);
   log2("   $char : $i, $result");
   $arr = array_values(explode(" of ", $result));
   if( count($arr) == 2) {
      $cmp = strcmp($arr[0],$arr[1]);
      return $cmp != 0;
   }
   return 0;
}

?>
