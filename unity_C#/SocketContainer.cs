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
public class ini_msg
{
    //public int messageID;
    //public int clientID;
    [MarshalAs(UnmanagedType.ByValArray, SizeConst = 50)] //限制50字节
    public byte[] message;
}
public class SocketContainer: MonoBehaviour
{
    string text;
    public Socket socketsend;
    static bool ready = true;
    // Start is called before the first frame update
    void Start()
    {
        
        socketsend = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        IPAddress ip = IPAddress.Parse("192.168.0.4");
        IPEndPoint point = new IPEndPoint(ip, 8080);
        socketsend.Connect(point);
        Debug.Log("连接成功！");

    }



}
