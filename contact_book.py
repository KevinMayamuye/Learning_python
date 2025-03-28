import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class ContactBookGUI:
    def __init__(self, master):
        self.master = master
        master.title("Contact Book")
        master.geometry("800x600")
        master.configure(bg='#f0f0f0')

        self.filename = "contacts.txt"  # File for storing contacts
        self.contacts = self.load_contacts()

        # Create UI Components
        self.create_widgets()   

    def load_contacts(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                return {}
        return {}

    def save_contacts(self):
        with open(self.filename, "w") as file:
            json.dump(self.contacts, file, indent=4)

    def create_widgets(self):
        # Frame for buttons

        button_frame = tk.Frame(self.master, bg='#f0f0f0')
        button_frame.pack(pady=10)

        # Buttons
        buttons = [
            ("Add Contact", self.add_contact),
            ("View Contacts", self.view_contacts),
            ("Search Contact", self.search_contact),
            ("Update Contact", self.update_contact),
            ("Delete Contact", self.delete_contact)
        ]

        for text, command in buttons:
            btn = tk.Button(button_frame, text=text, command=command, 
                            width=15, bg='#4CAF50', fg='white', 
                            font=('Arial', 10, 'bold'))
            btn.pack(side=tk.LEFT, padx=5)

        # Treeview to display contacts
        self.tree = ttk.Treeview(self.master, columns=('Name', 'Phone', 'Email', 'Address'), show='headings')
        self.tree.pack(padx=10, pady=10, expand=True, fill='both')

        # Define headings
        headings = [
            ('Name', 200),
            ('Phone', 150),
            ('Email', 200),
            ('Address', 200)
        ]

        for heading, width in headings:
            self.tree.heading(heading, text=heading)
            self.tree.column(heading, width=width, anchor='center')

        # Populate initial contacts
        self.update_contact_view()

    def add_contact(self):
        # Create a new window for adding contact
        add_window = tk.Toplevel(self.master)
        add_window.title("Add New Contact")
        add_window.geometry("400x300")

        # Labels and Entry fields
        labels = ["Name:", "Phone:", "Email:", "Address:"]
        entries = []

        for i, label_text in enumerate(labels):
            label = tk.Label(add_window, text=label_text)
            label.pack(pady=(10, 0))
            entry = tk.Entry(add_window, width=40)
            entry.pack()
            entries.append(entry)

        def save_new_contact():
            name = entries[0].get().strip()
            phone = entries[1].get().strip()
            email = entries[2].get().strip()
            address = entries[3].get().strip()

            # Validate input
            if not name:
                messagebox.showerror("Error", "Name cannot be empty!")
                return

            if name in self.contacts:
                messagebox.showerror("Error", f"Contact '{name}' already exists!")
                return

            # Save contact
            self.contacts[name] = {
                "phone": phone,
                "email": email,
                "address": address
            }
            self.save_contacts()
            self.update_contact_view()
            
            messagebox.showinfo("Success", f"Contact '{name}' added successfully!")
            add_window.destroy()

        # Save button
        save_btn = tk.Button(add_window, text="Save", command=save_new_contact)
        save_btn.pack(pady=10)

    def view_contacts(self):
        # This method is already handled by the Treeview update
        pass

    def update_contact_view(self):
        # Clear existing items

        for i in self.tree.get_children():
            self.tree.delete(i)

        # Populate with current contacts
        for name, details in self.contacts.items():
            self.tree.insert('', 'end', values=(
                name, 
                details.get('phone', 'N/A'), 
                details.get('email', 'N/A'), 
                details.get('address', 'N/A')
            ))

    def search_contact(self):
        name = simpledialog.askstring("Search", "Enter name to search:")
        if name and name in self.contacts:
            details = self.contacts[name]

            # Clear existing selection and select the matching contact
            for item in self.tree.get_children():
                if self.tree.item(item)['values'][0] == name:
                    self.tree.selection_set(item)
                    self.tree.focus(item)
                    self.tree.see(item)
                    break
            
            # Show details in a message box
            messagebox.showinfo("Contact Found", 
                f"Name: {name}\n"
                f"Phone: {details['phone']}\n"
                f"Email: {details.get('email', 'N/A')}\n"
                f"Address: {details.get('address', 'N/A')}")
        elif name:
            messagebox.showinfo("Search Result", f"No contact found with name '{name}'")

    def update_contact(self):

        # Get selected contact
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a contact to update")
            return

        name = self.tree.item(selected_item[0])['values'][0]
        details = self.contacts[name]

        # Create update window
        update_window = tk.Toplevel(self.master)
        update_window.title(f"Update Contact: {name}")
        update_window.geometry("400x300")

        # Labels and Entry fields pre-filled with current details
        labels = ["Name:", "Phone:", "Email:", "Address:"]
        entries = []

        values = [name, details['phone'], details.get('email', ''), details.get('address', '')]

        for i, (label_text, value) in enumerate(zip(labels, values)):
            label = tk.Label(update_window, text=label_text)
            label.pack(pady=(10, 0))
            entry = tk.Entry(update_window, width=40)
            entry.insert(0, value)
            entry.pack()
            entries.append(entry)

        def save_updated_contact():
            # Get new values
            new_name = entries[0].get().strip()
            new_phone = entries[1].get().strip()
            new_email = entries[2].get().strip()
            new_address = entries[3].get().strip()

            # Validate input
            if not new_name:
                messagebox.showerror("Error", "Name cannot be empty!")
                return

            # Remove old entry if name changed
            if new_name != name:
                del self.contacts[name]

            # Save updated contact
            self.contacts[new_name] = {
                "phone": new_phone,
                "email": new_email,
                "address": new_address
            }
            self.save_contacts()
            self.update_contact_view()
            
            messagebox.showinfo("Success", f"Contact updated successfully!")
            update_window.destroy()

        # Save button
        save_btn = tk.Button(update_window, text="Save", command=save_updated_contact)
        save_btn.pack(pady=10)

    def delete_contact(self):
        # Get selected contact

        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a contact to delete")
            return

        name = self.tree.item(selected_item[0])['values'][0]
        
        # Confirm deletion
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete contact '{name}'?")
        if confirm:
            del self.contacts[name]
            self.save_contacts()
            self.update_contact_view()
            messagebox.showinfo("Success", f"Contact '{name}' deleted successfully!")

def main():
    root = tk.Tk()
    app =  ContactBookGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()