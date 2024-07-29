from collections import OrderedDict
import json
from django.forms import model_to_dict
from idrecon.models import Contact
from django.core.exceptions import ObjectDoesNotExist

# def CreateContact(**kwargs):
#     email = kwargs.get('email', None)
#     phone_number = kwargs.get('phone_number', None)
#     return None

def handler(event):
    body = json.loads(event.body)
    req_email = body.get("email")
    req_phone = body.get("phoneNumber")

    if req_email is None and req_phone is None:
        resp = {"Error": "Invalid Request"}
        return resp
    
    elif req_email is None:
        matched_phone = Contact.objects.filter(phone_number=req_phone).first() #, link_precedence = Contact.LinkPrecedence.PRIMARY)
        if matched_phone is None:
            new_contact = Contact(phone_number=req_phone, link_precedence=Contact.LinkPrecedence.PRIMARY)
            new_contact.save()
            saved_contact = Contact.objects.get(phone_number=req_phone, link_precedence=Contact.LinkPrecedence.PRIMARY)
            matched_phone_pid = saved_contact.id
        else:
            if matched_phone.link_precedence == Contact.LinkPrecedence.PRIMARY:
                matched_phone_pid = matched_phone.id
            else:
                matched_phone_pid = matched_phone.linked_id
        primary_id = matched_phone_pid

    elif req_phone is None:
        matched_email = Contact.objects.filter(email=req_email).first()
        if matched_email is None:
            new_contact = Contact(email=req_email, link_precedence=Contact.LinkPrecedence.PRIMARY)
            new_contact.save()
            saved_contact = Contact.objects.get(email=req_email, link_precedence=Contact.LinkPrecedence.PRIMARY)
            matched_email_pid = saved_contact.id
        else:
            if matched_email.link_precedence == Contact.LinkPrecedence.PRIMARY:
                matched_email_pid = matched_email.id
            else:
                matched_email_pid = matched_email.linked_id
        primary_id = matched_email_pid

    else:
        matched_phone = Contact.objects.filter(phone_number=req_phone).first()
        matched_email = Contact.objects.filter(email=req_email).first()

        if matched_phone is None and matched_email is None:
            new_contact = Contact(phone_number=req_phone,
                                    email=req_email,
                                    link_precedence=Contact.LinkPrecedence.PRIMARY
                                )
            new_contact.save()
            saved_contact = Contact.objects.get(phone_number=req_phone,
                                    email=req_email,
                                    link_precedence=Contact.LinkPrecedence.PRIMARY
                                )
            matched_pid = saved_contact.id
        elif matched_email is None:
            if matched_phone.link_precedence == Contact.LinkPrecedence.PRIMARY:
                matched_phone_pid = matched_phone.id
            else:
                matched_phone_pid = matched_phone.linked_id
            new_contact = Contact(phone_number=req_phone,
                                    email=req_email,
                                    linked_id=matched_phone_pid,
                                    link_precedence=Contact.LinkPrecedence.SECONDARY
                                )
            new_contact.save()
            matched_pid = matched_phone_pid
        elif matched_phone is None:
            if matched_email.link_precedence == Contact.LinkPrecedence.PRIMARY:
                matched_email_pid = matched_email.id
            else:
                matched_email_pid = matched_email.linked_id
            new_contact = Contact(phone_number=req_phone,
                                    email=req_email,
                                    linked_id=matched_email_pid,
                                    link_precedence=Contact.LinkPrecedence.SECONDARY
                                )
            new_contact.save()
            matched_pid = matched_email_pid
        else:
            if matched_phone.id == matched_email.id:
                if matched_email.link_precedence == Contact.LinkPrecedence.PRIMARY:
                    matched_pid = matched_email.id
                else:
                    matched_pid = matched_email.linked_id
            else:
                # Get id of Primary of contact with Phone Number match
                if matched_phone.link_precedence == Contact.LinkPrecedence.PRIMARY:
                    matched_phone_pid = matched_phone.id
                else:
                    matched_phone_pid = matched_phone.linked_id

                # Get id of Primary of contact with email match
                if matched_email.link_precedence == Contact.LinkPrecedence.PRIMARY:
                    matched_email_pid = matched_email.id
                else:
                    matched_email_pid = matched_email.linked_id
                
                if matched_phone_pid > matched_email_pid:
                    # Get old Primary of contact with Phone Number match
                    matched_phone_op = Contact.objects.get(id=matched_phone_pid)
                    
                    # Set op to Secondary and link to new primary
                    matched_phone_op.link_precedence = Contact.LinkPrecedence.SECONDARY
                    matched_phone_op.linked_id = matched_email_pid
                    matched_phone_op.save()

                    matched_pid = matched_email_pid
                    # Link every secondary of op to new primary
                    Contact.objects.filter(linked_id=matched_phone_pid).update(linked_id=matched_pid)
                elif matched_phone_pid < matched_email_pid:
                    # Get old Primary of contact with email match
                    matched_email_op = Contact.objects.get(id=matched_email_pid)

                    # Set op to Secondary and link to new primary
                    matched_email_op.link_precedence = Contact.LinkPrecedence.SECONDARY
                    matched_email_op.linked_id = matched_phone_pid
                    matched_email_op.save()
                    
                    matched_pid = matched_phone_pid
                    # Link every secondary of op to new primary
                    Contact.objects.filter(linked_id=matched_email_pid).update(linked_id=matched_pid)
                else:
                    matched_pid = matched_phone_pid
        primary_id = matched_pid
        
 

    # Initialize the lists as empty
    email_array = []
    phone_array = []
    secondary_contact_ids = []

    # Get primary email and phone number
    try:
        primary_contact = Contact.objects.get(id=primary_id, link_precedence=Contact.LinkPrecedence.PRIMARY)
        email_array.append(primary_contact.email)
        phone_array.append(primary_contact.phone_number)
    except ObjectDoesNotExist:
        pass

    # Get all emails of this contact to include in response
    other_emails = Contact.objects.filter(linked_id=primary_id, link_precedence=Contact.LinkPrecedence.SECONDARY).values_list('email', flat=True)
    email_array.extend(other_emails)

    # Get all phone numbers of this contact to include in response
    other_phones = Contact.objects.filter(linked_id=primary_id, link_precedence=Contact.LinkPrecedence.SECONDARY).values_list('phone_number', flat=True)
    phone_array.extend(other_phones)

    secondary_contact_ids = list(Contact.objects.filter(linked_id=primary_id, link_precedence=Contact.LinkPrecedence.SECONDARY).values_list('id', flat=True))
    

    # Prepare response and return it
    contactResp = {
        "primaryContactID": primary_id,
        "emails": list(OrderedDict.fromkeys(email_array)),
        "phoneNumbers": list(OrderedDict.fromkeys(phone_array)),
        "secondaryContactIds": secondary_contact_ids
    }
    resp = {"contact": contactResp}
    return resp