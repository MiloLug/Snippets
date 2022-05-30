<?php
header('Access-Control-Allow-Origin: *');

require_once('horoshopGetter.php');
require_once('bitrixSetter.php');

$ordersToAdd = horoshop\getNewOrders();


foreach($ordersToAdd as $order){
	//if( 
		bitrix\addLead([
		"title" => $order["stat_created"],
		"name" => $order["delivery_name"],
		"currency" => $order["currency"],
		"total_price" => $order["total_sum"],
		"full_address" => $order["delivery_city"].", ".$order["delivery_address"],
		"phone" => $order["delivery_phone"],
		"products" => $order["products"]
	], [
		"UF_CRM_1600117903" => $order["delivery_city"].", ".$order["delivery_address"], //Адрес доставки
		"UF_CRM_1600117853" => $order["payment_type"]["title"], //Способ оплаты
		"UF_CRM_1600117842" => $order["delivery_type"]["title"], //Способ доставки
		"UF_CRM_1600121180" => $order["comment"] //Комментарий
	]);//["ok"] ) echo "ok<br/>";
}

//echo json_encode($ordersToAdd);

//echo json_encode(bitrix\getFields());
?>