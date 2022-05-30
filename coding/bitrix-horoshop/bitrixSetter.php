<?php namespace bitrix;

require_once('crest/crest.php');

//создаёт новый контакт с полученными данными и возвращает его айди, либо возвращает айдишник существующего с тем же номером
function addContact($name, $phone){	
	$res = \CRest::call(
		"crm.contact.add",[
			'fields' => [
				"NAME" => $name,
				"OPENED" => "Y",
				"ASSIGNED_BY_ID" => 1,
				"TYPE_ID" => "CLIENT",
				"SOURCE_ID" => "SELF",
				"PHONE" => [
					[
						"VALUE"=> $phone,
						"VALUE_TYPE"=> "WORK"
					]
			]
		],
		"params" => ["REGISTER_SONET_EVENT"=> "Y"]
	]);
	if(!isset($res["error"])){
		return [
			"ok" => true,
			"id" => $res["result"]
		];
	}else{
		return [
			"ok" => false,
			"error" => $res["error"]
		];
	}
}

function addProduct($name, $price, $currency){	
	$res = \CRest::call(
		"crm.product.list",[ 
			'filter' => [ "NAME" => $name],
			'select' => [ "ID", "PRICE"]
		]
	);
	
	if(!isset($res["error"]) && $res["total"] > 0){
		if($price == $res["result"][0]["PRICE"])		
			return [
				"ok" => true,
				"item" => ["PRODUCT_ID" => $res["result"][0]["ID"], "PRICE"=>$res["result"][0]["PRICE"]]
			];
		else{
			return [
				"ok" => true,
				"item" => ["PRODUCT_ID" => $res["result"][0]["ID"], "PRICE"=>$price]
			];
		}
	}
	
	$res = \CRest::call(
		"crm.product.add",[
			'fields' => [
				"NAME" => $name,
				"PRICE" => $price,
				"CURRENCY_ID" => $currency,
				"SORT" => 500
			]
		]);
	if(!isset($res["error"])){
		return [
			"ok" => true,
			"item" => ["PRODUCT_ID"=>$res["result"], "PRICE"=>$price]
		];
	}else{
		return [
			"ok" => false,
			"error" => $res["error"]
		];
	}
}

function setLeadProducts($leadID, $currency, $products = []){
	if(count($products) == 0)
		return;
	
	$rows = [];
	foreach($products as $prod){
		if($prod["price"] == 0)
			continue;
		
		$CRMprod = addProduct($prod["title"], $prod["price"], $currency);
		if($CRMprod["ok"]){
			$rows[] = [
				"PRODUCT_ID" => $CRMprod["item"]["PRODUCT_ID"],
				"PRICE" => $CRMprod["item"]["PRICE"],
				"QUANTITY" => $prod["quantity"]
			];
		}
	}
	if(count($rows) == 0)
		return;
	
	$res = \CRest::call(
		"crm.lead.productrows.set",[ 
			'id' => $leadID,
			'rows' => $rows
		]
	);
	
	if(!isset($res["error"])){
		return [
			"ok" => true
		];
	}else{
		return [
			"ok" => false,
			"error" => $res["error"]
		];
	}
}

function addLead($data, $custom_fields = []){
	$contact = addContact($data["name"], $data["phone"]);
	if(!$contact["ok"])
		return false;
	$contact = $contact["id"];
	
	
	$res = \CRest::call(
		"crm.lead.add",[ 
			'fields' => array_merge([
				"TITLE" => $data["title"], 
				"NAME" => $data["name"],
				"STATUS_ID" => "NEW",
				"OPENED" => "Y",
				"ASSIGNED_BY_ID" => 1,
				"CURRENCY_ID" => $data["currency"],
				"OPPORTUNITY" => $data["total_price"],
				"ADDRESS" => $data["full_address"],
				"PHONE" => [ [ "VALUE" => $data["phone"], "VALUE_TYPE" => "WORK" ] ],
				"CONTACT_ID" => $contact
			], $custom_fields),
			"params" => ["REGISTER_SONET_EVENT"=> "Y"]
		]
	);
	
	if(isset($res["error"])){
		return [
			"ok" => false,
			"error" => $res["error"]
		];
	}
	
	$res = setLeadProducts($res["result"], $data["currency"], $data["products"]);
	
	if(!isset($res["error"])){
		return [
			"ok" => true
		];
	}else{
		return [
			"ok" => false,
			"error" => $res["error"]
		];
	}
}

function getFields(){
	$res = \CRest::call(
		"crm.lead.fields",[]
	);
	
	if(!isset($res["error"])){
		return [
			"ok" => true,
			"fields" => $res["result"]
		];
	}else{
		return [
			"ok" => false,
			"error" => $res["error"]
		];
	}
}

?>