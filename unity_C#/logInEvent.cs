
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System;
using System.Runtime.InteropServices;

[Serializable]
[StructLayout(LayoutKind.Sequential, Pack = 1)]
public class kylo2
{
    //public int messageID;
    //public int clientID;
    //**********************************关键********************
    [MarshalAs(UnmanagedType.ByValArray, SizeConst = 15)] //这里只能填入需要的空间 不然接收端会出现乱码 不方便转码处理
    public byte[] message;
}
public class logInEvent : MonoBehaviour
{
    Socket socketsend;
    // List<byte> list = new List<byte>();
    // Use this for initialization\
    public GameObject Phone_number;
    public string text;
    public string phone;
    public static byte[] StructToBytes(object obj)
    {
        //得到结构体的大小
        int size = Marshal.SizeOf(obj);
        //创建byte数组
        byte[] bytes = new byte[size];
        //分配结构体大小的内存空间
        IntPtr structPtr = Marshal.AllocHGlobal(size);
        //将结构体拷到分配好的内存空间
        Marshal.StructureToPtr(obj, structPtr, false);
        //从内存空间拷到byte数组
        Marshal.Copy(structPtr, bytes, 0, size);
        //释放内存空间
        Marshal.FreeHGlobal(structPtr);
        //返回byte数组
        return bytes;
    }

    public void Start()
    {
        
        this.GetComponent<Button>().onClick.AddListener(OnClick_Register);
    }
    public void startThread()
    {
        try
        {

            //开启线程接收消息
            Thread th = new Thread(Recieve);
            th.IsBackground = true;
            th.Start();
        }
        catch
        {

            Debug.Log("初始化错误");
        }
    }
    public void OnClick_Register()
    {
       
        GameObject socketObject = GameObject.FindGameObjectWithTag("Socket");
        socketsend = socketObject.GetComponent<SocketContainer>().socketsend;
        Debug.Log("续接成功----");
 
        phone = Phone_number.GetComponent<TMP_InputField>().text;
        if(phone.Length != 11)
        {
            //弹出提醒框  手机号长度不正确
            Debug.Log("输入不正确，退出");
            return;
        }
          
        text = "Log-" + phone;
        Debug.Log(text);

        Send_Data();
  
    }
    public void Send_Data()
    {
        try
        {
            if (socketsend.Connected)
            {
                string str_Position = text;
                //Debug.Log("12"+str_Position);
                kylo2 ux = new kylo2();

                ux.message = Encoding.ASCII.GetBytes(str_Position);

                byte[] message_x = StructToBytes(ux);

                socketsend.Send(message_x);     
                Debug.Log("发送成功！");
                startThread();      //开启接收线程

            }
            else
            {
                Debug.Log("连接失败！");
            }

        }
        catch (SocketException se)
        {
            Debug.Log("发送失败！");
        }

    }
    //
    void Recieve()
    {
        while (true)
        {
            try
            {
                
                byte[] buffer = new byte[1024 * 1024 * 3];
                int r = socketsend.Receive(buffer);
                //if (r == 0)
                //{
                //    break;
                //    Environment.Exit(0);//结束当前进程

                //}
                string str = Encoding.UTF8.GetString(buffer, 0, r);

                Debug.Log("receive:" + str);
                str = str.Substring(0,4);
                if (String.Equals(str, "true"))
                {
                    Debug.Log("登录成功");
                }
                else
                {
                    Debug.Log("登录失败，手机号未注册");
                }

                break;


            }
            catch {

            }
        }
    }
}




