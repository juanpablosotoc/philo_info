import React from 'react';
import './App.css';
import Timeline from './components/timeline';
import TimelineEvent from './components/timelineEvent';
import Sequence from './components/sequence';
import SequenceEvent from './components/sequenceEvent';
import Quote from './components/quote';
import Audio from './components/audio';

function App() {
  const transcript = [{'word': 'Sure', 'start': 0.05999999865889549, 'end': 0.6000000238418579}, {'word': "I'll", 'start': 0.46000000834465027, 'end': 1.1399999856948853}, {'word': 'share', 'start': 1.1399999856948853, 'end': 1.340000033378601}, {'word': 'a', 'start': 1.340000033378601, 'end': 1.5399999618530273}, {'word': 'short', 'start': 1.5399999618530273, 'end': 1.940000057220459}, {'word': 'story', 'start': 1.940000057220459, 'end': 2.059999942779541}, {'word': 'with', 'start': 2.059999942779541, 'end': 2.319999933242798}, {'word': 'you', 'start': 2.319999933242798, 'end': 2.5399999618530273}, {'word': 'This', 'start': 3.180000066757202, 'end': 3.3399999141693115}, {'word': "one's", 'start': 3.3399999141693115, 'end': 3.5999999046325684}, {'word': 'a', 'start': 3.5999999046325684, 'end': 3.759999990463257}, {'word': 'classic', 'start': 3.759999990463257, 'end': 4.179999828338623}, {'word': 'fable', 'start': 4.179999828338623, 'end': 4.539999961853027}, {'word': 'The', 'start': 5.260000228881836, 'end': 5.340000152587891}, {'word': 'Tortoise', 'start': 5.340000152587891, 'end': 5.639999866485596}, {'word': 'and', 'start': 5.639999866485596, 'end': 5.840000152587891}, {'word': 'the', 'start': 5.840000152587891, 'end': 6.099999904632568}, {'word': 'Hare', 'start': 6.099999904632568, 'end': 6.159999847412109}, {'word': 'Once', 'start': 7.340000152587891, 'end': 7.480000019073486}, {'word': 'upon', 'start': 7.480000019073486, 'end': 7.699999809265137}, {'word': 'a', 'start': 7.699999809265137, 'end': 8.079999923706055}, {'word': 'time', 'start': 8.079999923706055, 'end': 8.199999809265137}, {'word': 'in', 'start': 8.4399995803833, 'end': 8.460000038146973}, {'word': 'a', 'start': 8.460000038146973, 'end': 8.899999618530273}, {'word': 'land', 'start': 8.899999618530273, 'end': 8.899999618530273}, {'word': 'filled', 'start': 8.899999618530273, 'end': 9.199999809265137}, {'word': 'with', 'start': 9.199999809265137, 'end': 9.5}, {'word': 'rolling', 'start': 9.5, 'end': 9.800000190734863}, {'word': 'hills', 'start': 9.800000190734863, 'end': 10.079999923706055}, {'word': 'and', 'start': 10.079999923706055, 'end': 10.4399995803833}, {'word': 'thick', 'start': 10.4399995803833, 'end': 10.680000305175781}, {'word': 'forests', 'start': 10.680000305175781, 'end': 11.180000305175781}, {'word': 'there', 'start': 11.739999771118164, 'end': 11.84000015258789}, {'word': 'lived', 'start': 11.84000015258789, 'end': 12.100000381469727}, {'word': 'a', 'start': 12.100000381469727, 'end': 12.600000381469727}, {'word': 'tortoise', 'start': 12.600000381469727, 'end': 12.600000381469727}, {'word': 'and', 'start': 12.600000381469727, 'end': 12.84000015258789}, {'word': 'a', 'start': 12.84000015258789, 'end': 13.100000381469727}, {'word': 'hare', 'start': 13.100000381469727, 'end': 13.100000381469727}, {'word': 'The', 'start': 13.720000267028809, 'end': 13.880000114440918}, {'word': 'hare', 'start': 13.880000114440918, 'end': 14.100000381469727}, {'word': 'with', 'start': 14.460000038146973, 'end': 14.539999961853027}, {'word': 'his', 'start': 14.539999961853027, 'end': 14.84000015258789}, {'word': 'sleek', 'start': 14.84000015258789, 'end': 15.140000343322754}, {'word': 'shiny', 'start': 15.65999984741211, 'end': 15.65999984741211}, {'word': 'fur', 'start': 15.65999984741211, 'end': 15.920000076293945}, {'word': 'and', 'start': 15.920000076293945, 'end': 16.239999771118164}, {'word': 'powerful', 'start': 16.239999771118164, 'end': 16.639999389648438}, {'word': 'legs', 'start': 16.639999389648438, 'end': 17.040000915527344}, {'word': 'would', 'start': 17.34000015258789, 'end': 17.440000534057617}, {'word': 'often', 'start': 17.440000534057617, 'end': 17.799999237060547}, {'word': 'boast', 'start': 17.799999237060547, 'end': 18.059999465942383}, {'word': 'about', 'start': 18.059999465942383, 'end': 18.3799991607666}, {'word': 'his', 'start': 18.3799991607666, 'end': 18.68000030517578}, {'word': 'speed', 'start': 18.68000030517578, 'end': 18.920000076293945}, {'word': 'He', 'start': 19.260000228881836, 'end': 19.360000610351562}, {'word': 'would', 'start': 19.360000610351562, 'end': 19.6200008392334}, {'word': 'leap', 'start': 19.6200008392334, 'end': 19.719999313354492}, {'word': 'and', 'start': 19.719999313354492, 'end': 20.18000030517578}, {'word': 'bound', 'start': 20.18000030517578, 'end': 20.280000686645508}, {'word': 'through', 'start': 20.280000686645508, 'end': 20.459999084472656}, {'word': 'the', 'start': 20.459999084472656, 'end': 21.0}, {'word': 'meadows', 'start': 21.0, 'end': 21.0}, {'word': 'showing', 'start': 21.639999389648438, 'end': 21.65999984741211}, {'word': 'off', 'start': 21.65999984741211, 'end': 21.860000610351562}, {'word': 'to', 'start': 21.860000610351562, 'end': 22.020000457763672}, {'word': 'all', 'start': 22.020000457763672, 'end': 22.239999771118164}, {'word': 'the', 'start': 22.239999771118164, 'end': 22.780000686645508}, {'word': 'animals', 'start': 22.780000686645508, 'end': 22.780000686645508}, {'word': 'and', 'start': 22.780000686645508, 'end': 23.18000030517578}, {'word': 'making', 'start': 23.18000030517578, 'end': 23.399999618530273}, {'word': 'fun', 'start': 23.399999618530273, 'end': 23.700000762939453}, {'word': 'of', 'start': 23.700000762939453, 'end': 23.84000015258789}, {'word': 'the', 'start': 23.84000015258789, 'end': 24.079999923706055}, {'word': 'slower', 'start': 24.079999923706055, 'end': 24.34000015258789}, {'word': 'ones', 'start': 24.34000015258789, 'end': 24.739999771118164}, {'word': 'especially', 'start': 25.3799991607666, 'end': 25.920000076293945}, {'word': 'the', 'start': 25.920000076293945, 'end': 26.299999237060547}, {'word': 'tortoise', 'start': 26.299999237060547, 'end': 26.6200008392334}, {'word': 'The', 'start': 27.040000915527344, 'end': 27.520000457763672}, {'word': 'tortoise', 'start': 27.520000457763672, 'end': 27.799999237060547}, {'word': 'on', 'start': 27.899999618530273, 'end': 28.020000457763672}, {'word': 'the', 'start': 28.020000457763672, 'end': 28.139999389648438}, {'word': 'other', 'start': 28.139999389648438, 'end': 28.34000015258789}, {'word': 'hand', 'start': 28.34000015258789, 'end': 28.6200008392334}, {'word': 'was', 'start': 28.6200008392334, 'end': 29.059999465942383}, {'word': 'calm', 'start': 29.059999465942383, 'end': 29.559999465942383}, {'word': 'and', 'start': 29.559999465942383, 'end': 30.100000381469727}, {'word': 'steady', 'start': 30.100000381469727, 'end': 30.399999618530273}, {'word': 'Though', 'start': 31.239999771118164, 'end': 31.280000686645508}, {'word': 'he', 'start': 31.280000686645508, 'end': 31.420000076293945}, {'word': 'was', 'start': 31.420000076293945, 'end': 31.6200008392334}, {'word': 'often', 'start': 31.6200008392334, 'end': 31.979999542236328}, {'word': 'mocked', 'start': 31.979999542236328, 'end': 32.2400016784668}, {'word': 'for', 'start': 32.2400016784668, 'end': 32.34000015258789}, {'word': 'his', 'start': 32.34000015258789, 'end': 32.65999984741211}, {'word': 'slowness', 'start': 32.65999984741211, 'end': 33.060001373291016}, {'word': 'he', 'start': 33.540000915527344, 'end': 33.65999984741211}, {'word': 'never', 'start': 33.65999984741211, 'end': 33.84000015258789}, {'word': 'let', 'start': 33.84000015258789, 'end': 34.040000915527344}, {'word': 'it', 'start': 34.040000915527344, 'end': 34.2400016784668}, {'word': 'bother', 'start': 34.2400016784668, 'end': 34.439998626708984}, {'word': 'him', 'start': 34.439998626708984, 'end': 34.70000076293945}, {'word': 'One', 'start': 35.619998931884766, 'end': 35.63999938964844}, {'word': 'sunny', 'start': 35.63999938964844, 'end': 35.939998626708984}, {'word': 'day', 'start': 35.939998626708984, 'end': 36.31999969482422}, {'word': 'tired', 'start': 36.939998626708984, 'end': 36.939998626708984}, {'word': 'of', 'start': 36.939998626708984, 'end': 37.099998474121094}, {'word': 'the', 'start': 37.099998474121094, 'end': 37.34000015258789}, {'word': "hare's", 'start': 37.34000015258789, 'end': 37.599998474121094}, {'word': 'bragging', 'start': 37.599998474121094, 'end': 37.91999816894531}, {'word': 'the', 'start': 38.380001068115234, 'end': 38.68000030517578}, {'word': 'tortoise', 'start': 38.68000030517578, 'end': 38.81999969482422}, {'word': 'challenged', 'start': 38.81999969482422, 'end': 39.279998779296875}, {'word': 'him', 'start': 39.279998779296875, 'end': 39.439998626708984}, {'word': 'to', 'start': 39.439998626708984, 'end': 39.619998931884766}, {'word': 'a', 'start': 39.619998931884766, 'end': 40.060001373291016}, {'word': 'race', 'start': 40.060001373291016, 'end': 40.060001373291016}, {'word': 'The', 'start': 40.619998931884766, 'end': 40.84000015258789}, {'word': 'hare', 'start': 40.84000015258789, 'end': 40.84000015258789}, {'word': 'laughed', 'start': 40.84000015258789, 'end': 41.18000030517578}, {'word': 'heartily', 'start': 41.18000030517578, 'end': 41.560001373291016}, {'word': 'at', 'start': 41.560001373291016, 'end': 41.720001220703125}, {'word': 'the', 'start': 41.720001220703125, 'end': 42.18000030517578}, {'word': 'idea', 'start': 42.18000030517578, 'end': 42.220001220703125}, {'word': 'but', 'start': 42.220001220703125, 'end': 42.52000045776367}, {'word': 'agreed', 'start': 42.52000045776367, 'end': 42.939998626708984}, {'word': 'thinking', 'start': 43.41999816894531, 'end': 43.41999816894531}, {'word': 'it', 'start': 43.41999816894531, 'end': 43.619998931884766}, {'word': 'would', 'start': 43.619998931884766, 'end': 43.7400016784668}, {'word': 'be', 'start': 43.7400016784668, 'end': 43.86000061035156}, {'word': 'an', 'start': 43.86000061035156, 'end': 44.08000183105469}, {'word': 'easy', 'start': 44.08000183105469, 'end': 44.279998779296875}, {'word': 'win', 'start': 44.279998779296875, 'end': 44.58000183105469}, {'word': 'The', 'start': 45.220001220703125, 'end': 45.900001525878906}, {'word': 'animals', 'start': 45.900001525878906, 'end': 46.2599983215332}, {'word': 'of', 'start': 46.2599983215332, 'end': 46.439998626708984}, {'word': 'the', 'start': 46.439998626708984, 'end': 46.959999084472656}, {'word': 'forest', 'start': 46.959999084472656, 'end': 46.959999084472656}, {'word': 'gathered', 'start': 46.959999084472656, 'end': 47.279998779296875}, {'word': 'to', 'start': 47.279998779296875, 'end': 47.959999084472656}, {'word': 'watch', 'start': 47.959999084472656, 'end': 47.959999084472656}, {'word': 'The', 'start': 48.58000183105469, 'end': 48.7599983215332}, {'word': 'starting', 'start': 48.7599983215332, 'end': 49.040000915527344}, {'word': 'point', 'start': 49.040000915527344, 'end': 49.279998779296875}, {'word': 'was', 'start': 49.279998779296875, 'end': 49.52000045776367}, {'word': 'set', 'start': 49.52000045776367, 'end': 49.65999984741211}, {'word': 'at', 'start': 49.65999984741211, 'end': 49.880001068115234}, {'word': 'one', 'start': 49.880001068115234, 'end': 50.13999938964844}, {'word': 'end', 'start': 50.13999938964844, 'end': 50.20000076293945}, {'word': 'of', 'start': 50.20000076293945, 'end': 50.36000061035156}, {'word': 'the', 'start': 50.36000061035156, 'end': 50.70000076293945}, {'word': 'meadow', 'start': 50.70000076293945, 'end': 50.70000076293945}, {'word': 'and', 'start': 50.959999084472656, 'end': 51.08000183105469}, {'word': 'the', 'start': 51.08000183105469, 'end': 51.279998779296875}, {'word': 'finish', 'start': 51.279998779296875, 'end': 51.5}, {'word': 'line', 'start': 51.5, 'end': 51.79999923706055}, {'word': 'was', 'start': 51.79999923706055, 'end': 52.0}, {'word': 'a', 'start': 52.0, 'end': 52.20000076293945}, {'word': 'large', 'start': 52.20000076293945, 'end': 52.560001373291016}, {'word': 'oak', 'start': 52.560001373291016, 'end': 52.779998779296875}, {'word': 'tree', 'start': 52.779998779296875, 'end': 52.97999954223633}, {'word': 'at', 'start': 52.97999954223633, 'end': 53.18000030517578}, {'word': 'the', 'start': 53.18000030517578, 'end': 53.31999969482422}, {'word': 'other', 'start': 53.31999969482422, 'end': 53.540000915527344}, {'word': 'end', 'start': 53.540000915527344, 'end': 53.79999923706055}, {'word': 'At', 'start': 54.2400016784668, 'end': 54.439998626708984}, {'word': 'the', 'start': 54.439998626708984, 'end': 54.720001220703125}, {'word': 'signal', 'start': 54.720001220703125, 'end': 54.86000061035156}, {'word': 'to', 'start': 54.86000061035156, 'end': 55.220001220703125}, {'word': 'start', 'start': 55.220001220703125, 'end': 55.400001525878906}, {'word': 'the', 'start': 55.400001525878906, 'end': 55.959999084472656}, {'word': 'hare', 'start': 55.959999084472656, 'end': 56.2599983215332}, {'word': 'zoomed', 'start': 56.2599983215332, 'end': 56.7400016784668}, {'word': 'off', 'start': 56.7400016784668, 'end': 57.08000183105469}, {'word': 'leaving', 'start': 57.84000015258789, 'end': 57.86000061035156}, {'word': 'a', 'start': 57.86000061035156, 'end': 58.13999938964844}, {'word': 'cloud', 'start': 58.13999938964844, 'end': 58.2599983215332}, {'word': 'of', 'start': 58.2599983215332, 'end': 58.720001220703125}, {'word': 'dust', 'start': 58.720001220703125, 'end': 58.720001220703125}, {'word': 'behind', 'start': 58.720001220703125, 'end': 59.099998474121094}, {'word': 'him', 'start': 59.099998474121094, 'end': 59.36000061035156}, {'word': 'The', 'start': 60.15999984741211, 'end': 60.2599983215332}, {'word': 'tortoise', 'start': 60.2599983215332, 'end': 60.58000183105469}, {'word': 'began', 'start': 60.58000183105469, 'end': 60.880001068115234}, {'word': 'his', 'start': 60.880001068115234, 'end': 61.15999984741211}, {'word': 'slow', 'start': 61.15999984741211, 'end': 61.65999984741211}, {'word': 'plodding', 'start': 61.97999954223633, 'end': 62.099998474121094}, {'word': 'journey', 'start': 62.099998474121094, 'end': 62.36000061035156}, {'word': 'towards', 'start': 62.36000061035156, 'end': 62.68000030517578}, {'word': 'the', 'start': 62.68000030517578, 'end': 62.91999816894531}, {'word': 'oak', 'start': 62.91999816894531, 'end': 63.099998474121094}, {'word': 'tree', 'start': 63.099998474121094, 'end': 63.380001068115234}, {'word': 'Halfway', 'start': 64.37999725341797, 'end': 64.5}, {'word': 'through', 'start': 64.5, 'end': 64.63999938964844}, {'word': 'the', 'start': 64.63999938964844, 'end': 65.16000366210938}, {'word': 'race', 'start': 65.16000366210938, 'end': 65.16000366210938}, {'word': 'confident', 'start': 65.5999984741211, 'end': 65.91999816894531}]
  return (
    <div className="App">
      <Timeline>
        <TimelineEvent color="primary" date='20/05/2005'><p><b>Something</b> happened</p></TimelineEvent>
        <TimelineEvent color="primary" date='20/05/2005'><p>Something <b>happened</b></p></TimelineEvent>
      </Timeline>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Age</th>
            <th>City</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>1</td>
            <td>Alice</td>
            <td>23</td>
            <td>New York</td>
          </tr>
          <tr>
            <td>2</td>
            <td>Bob</td>
            <td>30</td><td>San Francisco</td></tr><tr><td>3</td><td>Charlie</td><td>27</td><td>Los Angeles</td></tr><tr><td>4</td><td>Diana</td><td>22</td><td>Chicago</td></tr><tr><td>5</td><td>Edward</td><td>35</td><td>Houston</td></tr><tr><td>6</td><td>Fiona</td><td>28</td><td>Miami</td></tr></tbody></table>
      <Sequence>
      <SequenceEvent title='Some title'>
          <p><b>Something</b> happened</p>
        </SequenceEvent>
        <SequenceEvent title='Some title'>
          <p><b>Something</b> happened</p>
        </SequenceEvent>
        <SequenceEvent title='Some title'>
          <p><b>Something</b> happened</p>
        </SequenceEvent>
        <SequenceEvent title='Some title'>
          <p><b>Something</b> happened siu siu siu siu siu siu siu siu siu siu siuuuuuuu</p>
        </SequenceEvent>
        <SequenceEvent title='Some title'>
          <p><b>Something</b> happened</p>
        </SequenceEvent>
        <SequenceEvent title='Some title'>
          <p><b>Something</b> happened</p>
        </SequenceEvent>
        <SequenceEvent title='Some title'>
          <p><b>Something</b> happened</p>
        </SequenceEvent>
        <SequenceEvent title='Some title'>
          <p><b>Something</b> happened siu siu siu siu siu siu siu siu siu siu siuuuuuuu</p>
        </SequenceEvent>
      </Sequence>
      <Quote author='Jean Paul Soto'>
        Si pesa mas que un pollo me lo follo.
      </Quote>
      <Audio title='Some Title' transcript={transcript} src='https://factic-audios.s3.us-west-2.amazonaws.com/test.mp3'></Audio>
    </div>
  );
}

export default App;
