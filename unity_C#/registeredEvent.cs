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
    //**********************************�ؼ�********************
    [MarshalAs(UnmanagedType.ByValArray, SizeConst = 32)] //����ֻ��������Ҫ�Ŀռ� ��Ȼ���ն˻�������� ������ת�봦��
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
        //�õ��ṹ��Ĵ�С
        int size = Marshal.SizeOf(obj);
        //����byte����
        byte[] bytes = new byte[size];
        //����ṹ���С���ڴ�ռ�
        IntPtr structPtr = Marshal.AllocHGlobal(size);
        //���ṹ�忽������õ��ڴ�ռ�
        Marshal.StructureToPtr(obj, structPtr, false);
        //���ڴ�ռ俽��byte����
        Marshal.Copy(structPtr, bytes, 0, size);
        //�ͷ��ڴ�ռ�
        Marshal.FreeHGlobal(structPtr);
        //����byte����
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

            //�����߳̽�����Ϣ
            Thread th = new Thread(Recieve);
            th.IsBackground = true;
            th.Start();
        }
        catch
        {

            Debug.Log("��ʼ������");
        }
    }

    public void OnClick_Register()
    {
    
        GameObject socketObject = GameObject.FindGameObjectWithTag("Socket");
        socketsend = socketObject.GetComponent<SocketContainer>().socketsend;
        Debug.Log("���ӳɹ�----");

        
        phone = Phone_number.GetComponent<TMP_InputField>().text;
        active = Active_number.GetComponent<TMP_InputField>().text;
        if (phone.Length != 11)
        {
            //�������ѿ� �ֻ��ų��Ȳ���ȷ
            Debug.Log("���벻��ȷ���˳�");
            return;
        }
        else if (active.Length != 16)
        {
            //�������ѿ� �����볤�Ȳ���ȷ
            Debug.Log("���벻��ȷ���˳�");
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
                startThread();      //���������߳�
                //socketsend.Close();     //�ر�ͨѶ

            }
            else
            {
                Debug.Log("����ʧ�ܣ�");
            }

        }
        catch (SocketException se)
        {
            Debug.Log("����ʧ�ܣ�");
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
                //    Environment.Exit(0);//������ǰ����

                //}
                string str = Encoding.UTF8.GetString(buffer, 0, r);
                Debug.Log("receive:" + str);
                str = str.Substring(0, 4);
                if (str == "true")
                {
                    Debug.Log("ע��ɹ�");
                }
                else if(str == "fals")
                {
                    Debug.Log("ע��ʧ�ܣ����������");
                }
                break;


            }
            catch { }
        }
    }
}




