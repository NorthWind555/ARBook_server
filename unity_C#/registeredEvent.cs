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
public class kylo1
{
    //public int messageID;
    //public int clientID;
    //**********************************关键********************
    [MarshalAs(UnmanagedType.ByValArray, SizeConst = 32)] //这里只能填入需要的空间 不然接收端会出现乱码 不方便转码处理
    public byte[] message;
}
public class registeredEvent : MonoBehaviour
{
    Socket socketsend;
    // List<byte> list = new List<byte>();
    // Use this for initialization\
    public GameObject Phone_number;
    public GameObject Active_number;
    public string text;
    public string phone;
    public string active;
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
        active = Active_number.GetComponent<TMP_InputField>().text;
        if (phone.Length != 11)
        {
            //弹出提醒框 手机号长度不正确
            Debug.Log("输入不正确，退出");
            return;
        }
        else if (active.Length != 16)
        {
            //弹出提醒框 激活码长度不正确
            Debug.Log("输入不正确，退出");
            return;
        }

        text = "Reg-" + active + "-" + phone;
        Debug.Log(text);
        Send_Data();

    }
    void Send_Data()
    {
        try
        {
            if (socketsend.Connected)
            {
                string str_Position = text;
                //Debug.Log("12"+str_Position);
                kylo1 ux = new kylo1();
                ux.message = Encoding.ASCII.GetBytes(str_Position);

                byte[] message_x = StructToBytes(ux);

                socketsend.Send(message_x);
                startThread();      //开启接收线程
                //socketsend.Close();     //关闭通讯

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
                str = str.Substring(0, 4);
                if (str == "true")
                {
                    Debug.Log("注册成功");
                }
                else if(str == "fals")
                {
                    Debug.Log("注册失败，激活码错误");
                }
                break;


            }
            catch { }
        }
    }
}




