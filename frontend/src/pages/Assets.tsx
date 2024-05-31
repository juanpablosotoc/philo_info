import ShortTextInput from '../components/short_text_input/index';
import PasswordInput from '../components/password_input/index';
import SubmitBtn from '../components/submit_btn/index';
import OrLine from '../components/or_line/index';
import OAuth from '../components/oauth/index';
import UploadFile from '../components/upload_file/index';


function AssetsPage() {
    return (
      <div className="App">
        <ShortTextInput />
        <PasswordInput />
        <SubmitBtn />
        <br /><br />
        <OrLine />
        <OAuth type='apple'/>
        <OAuth type='google'/>
        <OAuth type='microsoft'/>
        <div className='black'>
          <UploadFile />
        </div>
      </div>
    );
  }

export default AssetsPage;
