**number** - целое число
**string** - строка
**symbol** - один символ
**identifier** - строка, связываемая как имя с соответствующим объектом
**identifier** - строка, соответствующая существующему идентификатору

**syntax** = «**number** : » **number** «; » {**define**} **test**
**define** = «**define** » **identifier** «(» [**identifier** {«, » **identifier**}] «) as » **test**
**parameter** = **number** | **real **| **string** | **test** | **identifier**
**define**d = **identifier** « { » [**identifier** « : » **parameter** {«; » **identifier** « : » **parameter**}] «}»
**test** = **integer** | **real **| **string** | **array** | **composite** | **choice** | **const** | **identifier** | **define**d
**numeric_type** = **number** | **identifier**
**real_type** = **real **| **identifier**
**integer** = «**integer** { min : » **numeric_type** «; max : » **numeric_type** [«; distribution : » (... | …)] [«; name : « **identifier**] « }»
**real **= «**real **{ min : » **real_type** «; max : » **real_type** [«; distribution : » (... | …)] [«; name : » **identifier**] « }»
**string** = «**string** { length : » (**integer** | **real_type**) [(«; allowed **symbol**s : » **symbol** {«,» **symbol**}) | («; forbidden **symbol**s : » **symbol** {«,» **symbol**})] [«; name : » **identifier**] « }»
**array** = «**array** { length : » (**integer** | **numeric_type**) «; type : » **test** [«; name : » **identifier**] « }»
**composite** = «**composite** { » **test** {«; » **test**} « }»
**choice** = «**choice** { » **test** «; » **test** {«; » **test**} « }»
**const** = «**const** { values :» **string** {«, » **string**} [«; name : » **identifier**] « }»

