import gzip



class SimilarityCalculator:
    def __init__(self, context_list:list, query:str) -> None:
        self.context_list = context_list
        self.query = query
    
    def _compute_distance(self):
        cx1  = len(gzip.compress(self.query.encode()))
        for context in self.context_list:
            cx2 = len(gzip.compress(context["text"].encode()))
            x1x2 = " ".join([self.query, context["text"]])
            cx1x2 = len(gzip.compress(x1x2.encode()))
            ncd = (cx1x2-min(cx1, cx2)) / max(cx1, cx2)
            context['distance'] = ncd
        return self.context_list
    
    def get_k_closest_result(self, k:int):
        print("Before:", self.context_list[0])
        sorted_list = sorted(self.context_list, key=lambda x: x['distance'])
        print("After:", self.context_list[0])
        
        return sorted_list[:k]
        

# context_list = [{"text":"TAI is an IT Company","source":"p"}, {"text":"Web&App is not a company","source":"p"}, {"text":"TAI has 70 empoyees.","source":"p"}]
# query = "what does tai do?"

# obj = SimilarityCalculator(context_list=context_list, query=query)
# final_compute = obj._compute_distance()
# print(final_compute)
# results = obj.get_k_closest_result(k=2)
# print(results)
        
            
            
        
        
