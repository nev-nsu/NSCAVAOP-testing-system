class Parser
{
	constructor (exec)
	{
		this.exec = function(str, pos)
		{
			if (pos > str.length)
				throw Error("Parser: position is out of range.");
			return exec(str, pos);
		}
	}

	then (transformation)
	{
		var ths = this;
		return new Parser(function (str, pos)
		{
			var result = ths.exec(str, pos);
			return result && { res: transformation(result.res), end: result.end };
		});
	}
}

/*---------------basic----------------------*/
var digit = new Parser(function(str, pos)
{
	var chr = str.charAt(pos);
	if (chr >= "0" && chr <= "9")
		return {
			res: chr,
			end: pos + 1
		};
});

function text (txt)
{
	return new Parser(function(str, pos)
	{
		if (str.substr(pos, txt.length) == txt)
			return {
				res: txt,
				end: pos + txt.length
			};
	});
}

function regexp (rgx)
{
	return new Parser(function(str, pos)
	{
		var m = rgx.exec(str.slice(pos));
		if (m && (m.index == 0))
			return {
				res: m[0],
				end: pos + m[0].length
			};
	});
}
/*------------------------------------------*/

/*---------------combined-------------------*/
function optional (parser)
{
	return new Parser(function(str, pos)
	{
		return parser.exec(str, pos) || { res: void 0, end: pos };
	});
}

// нигде не применяю
function exceptive (parser, exc_parser)
{
	return new Parser(function(str, pos)
	{
		return !exc_parser.exec(str, pos) && parser.exec(str, pos);
	});
}

function any ()
{
	var args = arguments;
	return new Parser(function(str, pos)
	{
		var result, n = args.length;
		for (var i = 0; i < n; i++)
		{
			if (result = args[i].exec(str, pos))
				return result;
		}
	});
}

function sequence ()
{
	var args = arguments;
	return new Parser(function(str, pos)
	{
		var result, res = [], end = pos, n = args.length;
		for (var i = 0; i < n; i++)
		{
			r = args[i].exec(str, end);
			if (!r) return;
			res.push(r.res);
			end = r.end;
		}
		return {
			res: res,
			end: end
		};
	});
}

function repetition (parser, separator)
{
	var separated = !separator ? parser : sequence(separator, parser).then(result => result[1]);
	return new Parser(function(str, pos)
	{
		var res = [], end = pos, result = parser.exec(str, end);
		// r.end > end зачем?
		// вроде, только optional может вернуть результат, не сдвинув end
		// такое условие как бы убивает весь смысл optional
		// (!) но если убрать это условие и запустить repetition(optional(...), ...), то зацикливание
		while (result && (result.end > end))
		{
			res.push(result.res);
			end = result.end;
			result = separated.exec(str, end);
		}

		if (res.length === 0)
			return;
		return {
			res: res,
			end: end
		}
	});
}
/*------------------------------------------*/

/*--------------another basics--------------*/
var natural_number = new Parser(function(str, pos)
{
	result = repetition(digit).then(res => parseInt(res.join(''), 10)).exec(str, pos);
	if (!result) return;
	if (result.res !== 0)
		return result;
});

var int_number = sequence(optional(text('-')), repetition(digit).then(res => res.join(''))).then(r => parseInt(r.join(''), 10));

var point = any(text('.'), text(',')).then(r => { if (r === ',') return '.'; else return r; });  // разделитель в вещественном числе
var real_number = sequence( int_number, optional( sequence(point, int_number).then(r=>r.join('')) ) ).then(r => parseFloat(r.join('')));

var q_mark = any(text('"'), text("'"));
var quoted = sequence( q_mark, id, q_mark ).then(r => r[1]);
/*------------------------------------------*/

/*------------------main--------------------*/
var id = regexp(/[a-z][^;,}"']*/i);

var field_name = regexp(/[a-z_]+/);

var number_of_tests = sequence(text('number:'), natural_number).then(result => result[1]);

var type = any( text('integer'), text('real'), text('string'), text('array'), text('composite'), text('choice'), text('const') );

var IDs = [];	//массив имен

function field(type)
{
	return new Parser(function(str, pos)
	{
		var res = [], end = pos;
		res[1] = {};
		var tmp = sequence(field_name, text(':')).then(r => r[0]).exec(str, end);
		if (!tmp)
			return void 0;
		res[0] = tmp.res;
		end = tmp.end;

		switch(type)
		{
			case 'integer':
				switch(res[0])
				{
					case 'min':
						tmp = any(int_number, id).exec(str, end);
						if (typeof(tmp.res) === 'string')
						{
							if (IDs.indexOf(tmp.res) === -1)
								throw new Error('Parser: the name "' + tmp.res + '" isn\'t defined.');
							res[1].type = 'variable';
							res[1].name = tmp.res;
						}
						else
						{
							res[1].type = 'value';
							res[1].value = tmp.res;
						}
						end = tmp.end;
						break;
					case 'max':
						tmp = any(int_number, id).exec(str, end);
						if (typeof(tmp.res) === 'string')
						{
							if (IDs.indexOf(tmp.res) === -1)
								throw new Error('Parser: the name "' + tmp.res + '" isn\'t defined.');
							res[1].type = 'variable';
							res[1].name = tmp.res;
						}
						else
						{
							res[1].type = 'value';
							res[1].value = tmp.res;
						}
						end = tmp.end;
						break;
					case 'name':
						tmp = id.exec(str, end);
						if (IDs.indexOf(tmp.res) !== -1)
							throw new Error('The name "' + tmp.res + '" is redefined.');
						IDs.push(tmp.res);
						res[1].type = 'value';
						res[1].value = tmp.res;
						end = tmp.end;
						break;
					default:
						// TODO
				}
				break;
			case 'real':
				switch(res[0])
				{
					case 'min':
						tmp = any(real_number, id).exec(str, end);
						if (typeof(tmp.res) === 'string')
						{
							if (IDs.indexOf(tmp.res) === -1)
								throw new Error('Parser: the name "' + tmp.res + '" isn\'t defined.');
							res[1].type = 'variable';
							res[1].name = tmp.res;
						}
						else
						{
							res[1].type = 'value';
							res[1].value = tmp.res;
						}
						end = tmp.end;
						break;
					case 'max':
						tmp = any(real_number, id).exec(str, end);
						if (typeof(tmp.res) === 'string')
						{
							if (IDs.indexOf(tmp.res) === -1)
								throw new Error('Parser: the name "' + tmp.res + '" isn\'t defined.');
							res[1].type = 'variable';
							res[1].name = tmp.res;
						}
						else
						{
							res[1].type = 'value';
							res[1].value = tmp.res;
						}
						end = tmp.end;
						break;
					case 'name':
						tmp = id.exec(str, end);
						if (IDs.indexOf(tmp.res) !== -1)
							throw new Error('The name "' + tmp.res + '" is redefined.');
						IDs.push(tmp.res);
						res[1].type = 'value';
						res[1].value = tmp.res;
						end = tmp.end;
						break;
					default:
						// TODO
				}
				break;
			case 'string':
				switch(res[0])
				{
					case 'length':
						tmp = any(natural_number, id).exec(str, end);
						if (typeof(tmp.res) === 'string')
						{
							if (IDs.indexOf(tmp.res) === -1)
								throw new Error('Parser: the name "' + tmp.res + '" isn\'t defined.');
							res[1].type = 'variable';
							res[1].name = tmp.res;
						}
						else
						{
							res[1].type = 'value';
							res[1].value = tmp.res;
						}
						end = tmp.end;
						break;
					case 'allowed_symbols':
						// TODO
						break;
					case 'forbidden_symbols':
						// TODO
						break;
					default:
						// TODO
				}
				break;
			case 'array':
				switch(res[0])
				{
					case 'length':
						tmp = any(natural_number, id).exec(str, end);
						if (typeof(tmp.res) === 'string')
						{
							if (IDs.indexOf(tmp.res) === -1)
								throw new Error('Parser: the name "' + tmp.res + '" isn\'t defined.');
							res[1].type = 'variable';
							res[1].name = tmp.res;
						}
						else
						{
							res[1].type = 'value';
							res[1].value = tmp.res;
						}
						end = tmp.end;
						break;
					case 'type':
						res[0] = 'element_type';
						tmp = test.exec(str, end);
						res[1].type = 'test';
						res[1].template = tmp.res;
						end = tmp.end;
						break;
					default:
						// TODO
				}
				break;
			case 'composite':
				// TODO
				break;
			case 'choice':
				// TODO
				break;
			case 'const':
				switch(res[0])
				{
					case 'value':
						tmp = quoted.exec(str, end);
						if (tmp)
						{
							res[1].type = 'value';
							res[1].value = tmp.res;
						}
						else
						{
							tmp = id.exec(str, end);
							if (IDs.indexOf(tmp.res) === -1)
								throw new Error('Parser: the name "' + tmp.res + '" isn\'t defined.');
							res[1].type = 'variable';
							res[1].name = tmp.res;
						}
						end = tmp.end;
						break;
					default:
						// TODO
						break;
				}
				break;
			default:
				// TODO
				break;
		}
			
		return {
			res: res,
			end: end
		}
	});
}

// вместо полей для тестов типов composite и choice
var tests_array =  new Parser(function(str, pos)
{
	var res = [], end = pos;
	res[1] = {};
	res[0] = 'array';

	tmp = repetition(test).exec(str, end);
	res[1].type = 'value';
	res[1].value = tmp.res;
	end = tmp.end;

	return {
		res: res,
		end: end
	}
});

// TODO test_field теперь возвращает другое
var test = new Parser(function(str, pos)
{
	var res = {}, end = pos;

	var tmp = sequence(type, text('{')).then(r => r[0]).exec(str, end);
	if (!tmp) return;
	res['type'] = {
		type: 'value',
		value: tmp.res
	};
	end = tmp.end;

	if (res.type.value === 'composite' || res.type.value === 'choice')
	{
		tmp = tests_array.exec(str, end);
		end = tmp.end;
		res[(tmp.res)[0]] = (tmp.res)[1];
	}
	else
	{
		tmp = repetition(field(res.type.value), text(';')).exec(str, end);
		end = tmp.end;
		var n = tmp.res.length;
		for (var i = 0; i < n; i++)
		{
			res[(tmp.res[i])[0]] = (tmp.res[i])[1];
		}
	}

	end = text('}').exec(str, end).end;
	return {
		res: res,
		end: end
	};
});

var note = new Parser(function(str, pos)
{
	IDs.splice(0, IDs.length);
	var res = {}, end = pos;

	var tmp = number_of_tests.exec(str, end);
	if (!tmp)
		return void 0;
	res['number'] = tmp.res;
	end = tmp.end;

	tmp = test.exec(str, end);
	end = tmp.end;
	res['template'] = tmp.res;

	return {
		res: res,
		end: end
	}
});

// использовать надо только это
var notes = repetition(note);

/*{
	"number": 20,
	"template": {
		"type": {
			"type": "value",
			"value": "composite"
		},
		"array": {
			"type": "value",
			"value": [
				{
					"type": {
						"type": "value",
						"value": "integer"
					},
					"min": {
						"type": "value",
						"value": 0
					},
					"max": {
						"type": "value",
						"value": 100
					}
				},
				{
					"type": {
						"type": "value",
						"value": "const"
					},
					"value": {
						"type": "value",
						"value": " "
					}
				},
				{
					"type": {
						"type": "value",
						"value": "integer"
					},
					"min": {
						"type": "value",
						"value": 0
					},
					"max": {
						"type": "value",
						"value": 100
					}
				},
				{
					"type": {
						"type": "value",
						"value": "const"
					},
					"value": {
						"type": "value",
						"value": " "
					}
				},
				{
					"type": {
						"type": "value",
						"value": "integer"
					},
					"min": {
						"type": "value",
						"value": 0
					},
					"max": {
						"type": "value",
						"value": 100
					}
				}
			]
		}
	}
}*/
