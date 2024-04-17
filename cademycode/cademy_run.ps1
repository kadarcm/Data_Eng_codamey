
$result =pytest .\cademycode\cademyPy\tests.py 


$loc= $result | Select-String 4\spassed
$log_file =".\cademycode\test_results\test_Pass_$(Get-Date -f  yyyy-MM-dd-HH-mm-ss).txt"
 if($loc.LineNumber -ge 0){
    $result | Out-File -Encoding "UTF8" $log_file
    Write-Host passed
    Write-Host "starting data pipeline"
    conda activate codemey 
    python  .\cademycode\cademyPy\program.py -f $log_file
 } else {
    $result | Out-File -Encoding "UTF8" $log_file
    Write-Host failed
 }
# cd ..
# cd ..

