<?php 

$ch = curl_init();
$link = ['link' => "https://www.amazon.in/dp/B09G9HD6PD/ref=redir_mobile_desktop?_encoding=UTF8&aaxitk=ef5999a9624cbf0717060ca6f1b989f2&hsa_cr_id=1681504330102&pd_rd_plhdr=t&pd_rd_r=6989883d-8966-47af-84a7-cbccd2ddfabf&pd_rd_w=loEXi&pd_rd_wg=5dWA9&ref_=sbx_be_s_sparkle_mcd_asin_0_title&th=1"];
curl_setopt($ch, CURLOPT_URL,"http://127.0.0.1:5000/");
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, $link);


// Receive server response ...
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$server_output = curl_exec($ch);

curl_close ($ch);

echo $server_output;


