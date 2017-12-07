
function MyForm(form_id) {
	this.name=$("#"+form_id+" .name");
	this.phone=$("#"+form_id+" .phone");
	this.email=$("#"+form_id+" .email");
	this.comment=$("#"+form_id+" .message");
	this.result=$("#resultContainer");
}

MyForm.prototype.clearErrorClass = function() {

	let fields=['name','phone','email','comment'];
	for(let i in fields) 
		this[fields[i]].removeClass('error');
	
}

MyForm.prototype.clearErrorStatus = function() {

	let fields=['name','phone','email','comment'];

	for(let i in fields) {
		if(this[fields[i]].next().hasClass('error-status')) 
			this[fields[i]].next().remove();		
	}
}

MyForm.prototype.setErrorStatus = function(obj) {

	let fields=['name','phone','comment'];
	let errorStatus = {
		name:"Корректно заполните имя.<br>Внимание: не допускается размещение ссылок на интернет-ресурсы",
		phone:"Введите номер телефона в заданном формате",
		email:"Введите email в заданном формате",
		comment:"Не допускается размещение ссылок на интернет-ресурсы"
	};

	for(let i in obj.errorFields) {
                this.result.append("<div class='error-status bg-warning'>"+errorStatus[obj.errorFields[i]]+"</div>");
		this[obj.errorFields[i]].addClass("error");
	}

}


MyForm.prototype.validate = function () {

	let emailtmpl = /[a-zA-Z0-9_\-\.]+@[a-z0-9]+\.(ru|ua|by|kz|com|[a-z]{2,3}|рф)/;
	let phonetmpl = /^\+?[78]?[\-\s]?\(?\d{3}\)?[\-\s]?\d\d\d[\-\s]?\d\d[\-\s]?\d\d$/;
	let urltmpl = /(http[s]?:\/\/)?(www\.)?[a-z0-9а-я_\-]+\.(ru|ua|by|kz|com|[a-z]{2,3}|рф)/;
	
	let obj = {'isValid': true, 'errorFields':[]};

	var x=this.name.val().trim();
	if(x.length==0 || x.length>30 || urltmpl.test(x)) {
		obj.isValid=false;	
		obj.errorFields.push('name');
	}			

	var x=this.email.val().trim();
	if(!emailtmpl.test(x.trim()) || x==="") {
		obj.isValid=false;	
		obj.errorFields.push('email');
	}

	var x=this.phone.val().trim();
	if(!phonetmpl.test(x.trim()) || x==="") {
		obj.isValid=false;	
		obj.errorFields.push('phone');
	}

	if(urltmpl.test(this.comment.val().trim())) {
		obj.isValid=false;	
		obj.errorFields.push('comment');
	}   

	return obj;
}
MyForm.prototype.setData = function(f) {
	this.name.val(f.name);
	this.email.val(f.email);
	this.phone.val(f.phone);
	this.comment.val(f.comment);
}
MyForm.prototype.serialize = function() {
	return 'name='+this.name.val()+'&email='+this.email.val()+'&phone='+this.phone.val()+'&comment='+this.comment.val()+'';
}

MyForm.prototype.printResponse= function(data) {
	this.result.removeClass("success");	
	this.result.removeClass("error");	
	this.result.addClass(data.status);
	this.result.html(data.response);	
}
MyForm.prototype.submit = function() {
	let validRes=this.validate();			
	this.clearErrorClass();
	this.clearErrorStatus();
	this.result.html('');

	if(!validRes.isValid) {
		this.setErrorStatus(validRes);
	}
	else {
		let that=this;
		$.ajax({		
			url: "form_ajax.php",
			type:"POST", 
//			dataType: "json", 
			data: this.serialize(), 
			success: function(data) {
				data=JSON.parse(data);
				console.log(data);
				console.log(that);
				that.printResponse(data);
			},
			error:  function(xhr, str){
				let obj={'status':"error",'response':"Ошибка обработки запроса."};
				that.printResponse(obj);
			}
		});   
	}
}

