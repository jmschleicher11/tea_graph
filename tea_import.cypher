CALL apoc.load.json("file:///all_tea_info.json")
yield value
UNWIND value.items AS item
merge (t:tea {id: item.id})
set t.name = item.name,
    t.short_id = item.short_id,
    t.min_price = item.min_price
with t, item
merge (o:origin {name: item.origin})
merge (o)<-[:COMES_FROM]-(t)
merge (ty:type {name: item.type})
merge (ty)<-[:TYPE_OF]-(t)
with t, item
unwind item.ingredients as ingredient
merge (i:ingredient {name: ingredient})
merge (i)<-[:MADE_WITH]-(t)
with t, item
unwind item.tags as tag
merge (ta:tag {name: tag})
merge (ta)<-[:TAGGED_WITH]-(t)
