
$result =pytest .\cademycode\cademyPy\tests.py 


$loc= $result | Select-String 4\spassed
 if($loc.LineNumber -ge 0){
    $result | Out-File ".\cademycode\test_results\test_Pass_$(Get-Date -f  yyyy-MM-dd-HH-mm-ss).txt"
    Write-Host passed
 } else {
    $result | Out-File ".\cademycode\test_results\test_Fail_$(Get-Date -f  yyyy-MM-dd-HH-mm-ss).txt"
    Write-Host failed
 }
# cd ..
# cd ..

