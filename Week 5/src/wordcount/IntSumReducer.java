package wordcount;

import java.io.IOException;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class IntSumReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
    private IntWritable result = new IntWritable();

    public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
        int sum = 0;
        // Duyệt qua danh sách các số 1 của cùng một từ để cộng dồn
        for (IntWritable val : values) {
            sum += val.get();
        }
        result.set(sum);
        // Ghi kết quả cuối cùng ra file: (word, tổng_số_lượng)
        context.write(key, result);
    }
}