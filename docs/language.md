**number** - целое число
**real_number** - нецелое число
**string** - строка
**symbol** - один символ
**identifier** - строка, связываемая как имя с соответствующим объектом

**syntax** = «number: » **number** «; » {**define**} **test**

**define** = «define » **identifier** «(» [**identifier** {«, » **identifier**}] «) as » **test**

**parameter** = **number** | **real **| **string** | **test** | **identifier**

**define** = **identifier** « { » [**identifier** « : » **parameter** {«; » **identifier** « : » **parameter**}] «}»

**test** = **integer** | **real **| **string** | **array** | **composite** | **choice** | **const** | **identifier** | **define**

**numeric_type** = **number** | **identifier** | **integer**

**real_type** = **real** | **identifier** | **real_number**

**integer** = «integer { min : » **numeric_type** «; max : » **numeric_type** [«; distribution : » (... | …)] [«; name : « **identifier**] « }»

**real **= «real { min : » **real_type** «; max : » **real_type** [«; distribution : » (... | …)] [«; name : » **identifier**] « }»

**string** = «string { length : » **numeric_type** [(«; allowed: » **symbol** {«,» **symbol**}) | («; forbidden: » **symbol** {«,» **symbol**})] [«; name : » **identifier**] « }»

**array** = «**array** { length : » **numeric_type** «; element_type : » **test** [«; name : » **identifier**] « }»

**composite** = «composite { » **test** {«; » **test**} « }»

**choice** = «choice { » **test** «; » **test** {«; » **test**} « }»

**const** = «const { value :» **string** [«; name : » **identifier**] « }»

