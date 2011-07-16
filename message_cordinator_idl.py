# Python stubs generated by omniidl from message_cordinator.idl

import omniORB, _omnipy
from omniORB import CORBA, PortableServer
_0_CORBA = CORBA

_omnipy.checkVersion(3,0, __file__)


#
# Start of module "Messaging"
#
__name__ = "Messaging"
_0_Messaging = omniORB.openModule("Messaging", r"message_cordinator.idl")
_0_Messaging__POA = omniORB.openModule("Messaging__POA", r"message_cordinator.idl")


# interface Receiver
_0_Messaging._d_Receiver = (omniORB.tcInternal.tv_objref, "IDL:Messaging/Receiver:1.0", "Receiver")
omniORB.typeMapping["IDL:Messaging/Receiver:1.0"] = _0_Messaging._d_Receiver
_0_Messaging.Receiver = omniORB.newEmptyClass()
class Receiver :
    _NP_RepositoryId = _0_Messaging._d_Receiver[1]

    def __init__(self, *args, **kw):
        raise RuntimeError("Cannot construct objects of this type.")

    _nil = CORBA.Object._nil


_0_Messaging.Receiver = Receiver
_0_Messaging._tc_Receiver = omniORB.tcInternal.createTypeCode(_0_Messaging._d_Receiver)
omniORB.registerType(Receiver._NP_RepositoryId, _0_Messaging._d_Receiver, _0_Messaging._tc_Receiver)

# Receiver operations and attributes
Receiver._d_send = ((omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_long), (), None)
Receiver._d_get_id = ((), (omniORB.tcInternal.tv_long, ), None)

# Receiver object reference
class _objref_Receiver (CORBA.Object):
    _NP_RepositoryId = Receiver._NP_RepositoryId

    def __init__(self):
        CORBA.Object.__init__(self)

    def send(self, *args):
        return _omnipy.invoke(self, "send", _0_Messaging.Receiver._d_send, args)

    def get_id(self, *args):
        return _omnipy.invoke(self, "get_id", _0_Messaging.Receiver._d_get_id, args)

    __methods__ = ["send", "get_id"] + CORBA.Object.__methods__

omniORB.registerObjref(Receiver._NP_RepositoryId, _objref_Receiver)
_0_Messaging._objref_Receiver = _objref_Receiver
del Receiver, _objref_Receiver

# Receiver skeleton
__name__ = "Messaging__POA"
class Receiver (PortableServer.Servant):
    _NP_RepositoryId = _0_Messaging.Receiver._NP_RepositoryId


    _omni_op_d = {"send": _0_Messaging.Receiver._d_send, "get_id": _0_Messaging.Receiver._d_get_id}

Receiver._omni_skeleton = Receiver
_0_Messaging__POA.Receiver = Receiver
omniORB.registerSkeleton(Receiver._NP_RepositoryId, Receiver)
del Receiver
__name__ = "Messaging"

# typedef ... ReceiverSeq
class ReceiverSeq:
    _NP_RepositoryId = "IDL:Messaging/ReceiverSeq:1.0"
    def __init__(self, *args, **kw):
        raise RuntimeError("Cannot construct objects of this type.")
_0_Messaging.ReceiverSeq = ReceiverSeq
_0_Messaging._d_ReceiverSeq  = (omniORB.tcInternal.tv_sequence, omniORB.typeMapping["IDL:Messaging/Receiver:1.0"], 0)
_0_Messaging._ad_ReceiverSeq = (omniORB.tcInternal.tv_alias, ReceiverSeq._NP_RepositoryId, "ReceiverSeq", (omniORB.tcInternal.tv_sequence, omniORB.typeMapping["IDL:Messaging/Receiver:1.0"], 0))
_0_Messaging._tc_ReceiverSeq = omniORB.tcInternal.createTypeCode(_0_Messaging._ad_ReceiverSeq)
omniORB.registerType(ReceiverSeq._NP_RepositoryId, _0_Messaging._ad_ReceiverSeq, _0_Messaging._tc_ReceiverSeq)
del ReceiverSeq

# interface Coordinator
_0_Messaging._d_Coordinator = (omniORB.tcInternal.tv_objref, "IDL:Messaging/Coordinator:1.0", "Coordinator")
omniORB.typeMapping["IDL:Messaging/Coordinator:1.0"] = _0_Messaging._d_Coordinator
_0_Messaging.Coordinator = omniORB.newEmptyClass()
class Coordinator :
    _NP_RepositoryId = _0_Messaging._d_Coordinator[1]

    def __init__(self, *args, **kw):
        raise RuntimeError("Cannot construct objects of this type.")

    _nil = CORBA.Object._nil


_0_Messaging.Coordinator = Coordinator
_0_Messaging._tc_Coordinator = omniORB.tcInternal.createTypeCode(_0_Messaging._d_Coordinator)
omniORB.registerType(Coordinator._NP_RepositoryId, _0_Messaging._d_Coordinator, _0_Messaging._tc_Coordinator)

# Coordinator operations and attributes
Coordinator._d_register = ((omniORB.typeMapping["IDL:Messaging/Receiver:1.0"], ), (omniORB.tcInternal.tv_long, ), None)
Coordinator._d_unregister = ((omniORB.tcInternal.tv_long, ), (), None)
Coordinator._d_ready = ((), (omniORB.tcInternal.tv_boolean, ), None)
Coordinator._d_receivers = ((), (omniORB.typeMapping["IDL:Messaging/ReceiverSeq:1.0"], ), None)

# Coordinator object reference
class _objref_Coordinator (CORBA.Object):
    _NP_RepositoryId = Coordinator._NP_RepositoryId

    def __init__(self):
        CORBA.Object.__init__(self)

    def register(self, *args):
        return _omnipy.invoke(self, "register", _0_Messaging.Coordinator._d_register, args)

    def unregister(self, *args):
        return _omnipy.invoke(self, "unregister", _0_Messaging.Coordinator._d_unregister, args)

    def ready(self, *args):
        return _omnipy.invoke(self, "ready", _0_Messaging.Coordinator._d_ready, args)

    def receivers(self, *args):
        return _omnipy.invoke(self, "receivers", _0_Messaging.Coordinator._d_receivers, args)

    __methods__ = ["register", "unregister", "ready", "receivers"] + CORBA.Object.__methods__

omniORB.registerObjref(Coordinator._NP_RepositoryId, _objref_Coordinator)
_0_Messaging._objref_Coordinator = _objref_Coordinator
del Coordinator, _objref_Coordinator

# Coordinator skeleton
__name__ = "Messaging__POA"
class Coordinator (PortableServer.Servant):
    _NP_RepositoryId = _0_Messaging.Coordinator._NP_RepositoryId


    _omni_op_d = {"register": _0_Messaging.Coordinator._d_register, "unregister": _0_Messaging.Coordinator._d_unregister, "ready": _0_Messaging.Coordinator._d_ready, "receivers": _0_Messaging.Coordinator._d_receivers}

Coordinator._omni_skeleton = Coordinator
_0_Messaging__POA.Coordinator = Coordinator
omniORB.registerSkeleton(Coordinator._NP_RepositoryId, Coordinator)
del Coordinator
__name__ = "Messaging"

#
# End of module "Messaging"
#
__name__ = "message_cordinator_idl"

_exported_modules = ( "Messaging", )

# The end.
