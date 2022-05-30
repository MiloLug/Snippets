<?php namespace horoshop;

$token = 0;
$API_password = "t2tvAPI_Pgkww23";
$API_username = "t2tvAPI";
$API_url = 'https://t2-tv.com.ua/api/';

function JSONrequest($url, $data){
	$ch = curl_init($url);
	$payload = json_encode($data);
	curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
	curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type:application/json'));
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	$result = curl_exec($ch);
	curl_close($ch);
	return json_decode($result, true);
}

function APIRequest($method, $data = []){
	global $token, $API_password, $API_username, $API_url;
	$req;
	if($token === 0){
		$req = JSONrequest($API_url . "auth/", [
			"login" => $API_username,
   			"password" => $API_password
		]);
		if($req["status"] != "OK")
			return $req;
		
		$token = $req["response"]["token"];
	}
	
	$args = array_merge([
		"token" => $token
	], $data);
	
	
	$req = JSONrequest($API_url . $method."/", $args);
	
	return $req;
}


function getOrders(){
	$fromDate = new \DateTime();
	$fromDate->sub(new \DateInterval("P2D"));
	return APIRequest("orders/get", [
		"status" => 6,
		"from" => $fromDate->format('Y-m-d'),
		"limit" => 1000
	]);
}
/*
function quicksort($arr, $first, $last) {
	$midIndex = intval(($first + $last) / 2);
	$mid = $arr[$midIndex];
	$_first = $first;
	$_last = $last;
	$tmp;

	while ($_first < $_last) {
		while ($arr[$_first] < $mid) $_first++;
		while ($arr[$_last] > $mid) $_last--;

		if ($_first <= $_last) {
			$tmp = $arr[$_first];
			$arr[$_first] = $arr[$_last];
			$arr[$_last] = $tmp;
			$_first++;
			$_last--;
		}
	}

	if ($first < $_last) quicksort($arr, $first, $_last);
	if ($_first < $last) quicksort($arr, $_first, $last);
}
*/

function interSearch(&$arr, $size, $key) {
	$mid;
	$low = 0;
	$high = $size - 1;
	if ($size < 1 || $key > $arr[$high] || $key < $arr[$low])
		return -1;

	while ($arr[$high] != $arr[$low]) {
		$mid = $low + intval((($high - $low) * ($key - $arr[$low])) / ($arr[$high] - $arr[$low]));

		if ($arr[$mid] < $key)
			$low = $mid + 1;
		else if ($arr[$mid] > $key)
			$high = $mid - 1;
		else
			return $mid;
	}

	if ($arr[$low] == $key)
		return $low;
	if ($arr[$high] == $key)
		return $high;

	return -1;
}

function getNewOrders(){
	$orders = getOrders();
	if($orders["status"] != "OK")
		return;
	$orders = $orders["response"]["orders"];
	$ordersCount = count($orders);
	
	$leashedArr = array_fill(0, $ordersCount, 0);
	$testArr = json_decode(file_exists("testArr") ? file_get_contents("testArr") : '[]', true);
	$testArrCount = count($testArr);
	$prevFound = $testArrCount; //для сужения зоны поиска
	
	$newOrders = [];
	
	for($i = 0; $i < $ordersCount; $i++){
		$leashedArr[$ordersCount - $i - 1] = $orders[$i]["order_id"];
		
		$found = interSearch($testArr, $prevFound, $orders[$i]["order_id"]);
		if($found === -1){
			$newOrders[] = $orders[$i];
		}else{
			$prevFound = $found;
		}
	}
	
	file_put_contents("testArr", json_encode($leashedArr));
	
	return $newOrders;
}
?>