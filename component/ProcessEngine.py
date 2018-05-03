from pyspark import SparkContext,SparkConf
class ProcessEngine():
    def __init__(self,appName):
        self.__rdd=None
        self.__appName=appName
    def execute(self,processConfig):
        for head in processConfig:
            if head["nodeName"]=="init":
                self.__rdd=self.__init(head)
            elif head["nodeName"]=="flatMap":
                self.__rdd= self.__flatMap(head,self.__rdd)
            elif head["nodeName"]=="map":
                self.__rdd= self.__map(head,self.__rdd)
            elif head["nodeName"]=="reduceByKey":
                self.__rdd= self.__reduceByKey(head,self.__rdd)
            elif head["nodeName"]=="filter":
                self.__rdd= self.__filter(head,self.__rdd)
            elif head["nodeName"]=="saveAsTextFile":
                self.__saveAsTextFile(head,self.__rdd)
            elif head["nodeName"]=="coalesce":
                self.__coalesce(head,self.__rdd)
    def __init(self,nodeMap):
        conf=SparkConf().setAppName(self.__appName)
        return SparkContext(conf=conf).textFile(nodeMap["path"])
    def __flatMap(self,nodeMap,rdd):
        return rdd.flatMap(eval(nodeMap["operation"]))
    def __map(self,nodeMap,rdd):
        return rdd.map(eval(nodeMap["operation"]))
    def __reduceByKey(self,nodeMap,rdd):
        return rdd.reduceByKey(eval(nodeMap["operation"]))
    def __filter(self,nodeMap,rdd):
        return rdd.filter(eval(nodeMap["operation"]))
    def __saveAsTextFile(self,nodeMap,rdd):
        import time
        rdd.saveAsTextFile(nodeMap["operation"]+"/"+self.__appName+"-"+time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())))
    def __coalesce(self,nodeMap,rdd):
        return rdd.coalesce(eval(nodeMap["operation"]))