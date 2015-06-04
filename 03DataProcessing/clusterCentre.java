import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.log4j.Logger;
import org.apache.spark.api.java.*;
import org.apache.spark.api.java.function.Function;
import org.apache.spark.mllib.clustering.KMeans;
import org.apache.spark.mllib.clustering.KMeansModel;
import org.apache.spark.mllib.linalg.Vector;
import org.apache.spark.mllib.linalg.Vectors;
import org.apache.spark.SparkConf;

/*
* This class takes the given set of coordinates as input
* and calcuate a number of cluster centres base on user preference
* all points will be categorized to a claster and output result
*/
public class KMeansExample {
  public static void main(String[] args) {
    SparkConf conf = new SparkConf().setAppName("K-means Example").setMaster("local");
    JavaSparkContext sc = new JavaSparkContext(conf);

    // Load and parse data
    String path = "coords.txt";
    JavaRDD<String> data = sc.textFile(path);
    JavaRDD<Vector> parsedData = data.map(new Function<String, Vector>() {
      public Vector call(String s) {
        String[] sarray = s.split(" ");
        double[] values = new double[sarray.length];
        for (int i = 0; i < sarray.length; i++)
          values[i] = Double.parseDouble(sarray[i]);
        return Vectors.dense(values);
      }
    });
    parsedData.cache();

    // Cluster the data into two classes using KMeans
    int numClusters = 50;
    int numIterations = 20;
    KMeansModel clusters = KMeans.train(parsedData.rdd(), numClusters, numIterations);

    Vector[] v = clusters.clusterCenters();
    clusters.predict(parsedData).map(new Function<Integer, String>() {
      public String call(Integer x) {
        return v[x].toString().replace("[", "").replace("]", "");
      }
    }).saveAsTextFile("KMeans");
  }
}